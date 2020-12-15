"""
.. module:: Get_Trello_MoodleEPN_Keys
   :platform: Unix, Windows
   :synopsis: This module gets keys, and initializes config files.

.. moduleauthor:: Luis Andrade <andr3slelouch@github.com>


"""
# This code is based on https://github.com/delucks/gtd.py onboard function,
# especial thanks to: delucks
import yaml
import os
import webbrowser
import trello
import sys
from polical import configuration
from polical import connectSQLite
from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied
import logging

logging.basicConfig(
    filename=configuration.get_file_location("Running.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class DevNullRedirect:
    """Temporarily eat stdout/stderr to allow no output.
    This is used to suppress browser messages in webbrowser.open"""

    def __enter__(self):
        self.old_stderr = os.dup(2)
        self.old_stdout = os.dup(1)
        os.close(2)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)

    def __exit__(self, exc_type, exc_value, traceback):
        os.dup2(self.old_stderr, 2)
        os.dup2(self.old_stdout, 1)


def onboard(no_open: bool, output_path="polical.yaml"):
    """Obtain Trello API credentials and put them into your config file.
    This is invoked automatically the first time you attempt to do an operation which requires authentication.
    The configuration file is put in an appropriate place for your operating system.
    """
    username = ""
    output_file = configuration.get_file_location(output_path)  # Use platform detection
    user_api_key_url = "https://trello.com/app-key"
    request_token_url = "https://trello.com/1/OAuthGetRequestToken"
    authorize_url = "https://trello.com/1/OAuthAuthorizeToken"
    access_token_url = "https://trello.com/1/OAuthGetAccessToken"
    calendar_moodle_epn_url = "https://aulasvirtuales.epn.edu.ec/calendar/export.php?"
    # Nuevo link https://aulasvirtuales.epn.edu.ec/calendar/export.php?
    # First, open the URL that allows the user to get an auth token. Tell them to copy both into the program
    logging.info("Mostrando print-board al usuario")
    print(
        "Bienvenido a PoliCal!\n Recuerde que antes de iniciar el proceso de obtención de credenciales ud debe tener una cuenta en Trello y en el Aula Virtual, y deben estar iniciadas las sesiones en el navegador predeterminado"
    )
    print("")
    print("\n\n")
    username = input("Ingrese su nombre:")
    print("PASO 1: Acceso a Trello")
    print("Recuerde ingresar e iniciar sesion previamente a www.trello.com")
    print("En su navegador web se cargará el siguiente URL:")
    print("  " + user_api_key_url)
    print(
        'Cuando llegue a esa página, inicie sesión y copie la "Tecla" o "Key" que se muestra en un cuadro de texto.'
    )
    print(
        "Si es la primera vez que realiza este proceso debe aceptar los terminos y condiciones de Trello"
    )
    input("Presione ENTER para ir al enlace")
    if not no_open:
        with DevNullRedirect():
            webbrowser.open_new_tab(user_api_key_url)
    api_key = input('Por favor, introduzca el valor de "Tecla" o "Key":')
    print(
        'Ahora desplácese hasta la parte inferior de la página y copie el "Secreto" o "Secret" que se muestra en un cuadro de texto.'
    )
    api_secret = input('Por favor, introduzca el valor de "Secret":')
    # Then, work on getting OAuth credentials for the user so they are permanently authorized to use this program
    print("\n\n")
    print("PASO 2: Permitir acceso de Polical a Trello")
    print(
        "Ahora obtendremos las credenciales de OAuth necesarias para usar este programa..."
    )
    # The following code is cannibalized from trello.util.create_oauth_token from the py-trello project.
    # Rewriting because it does not support opening the auth URLs using webbrowser.open and since we're using
    # click, a lot of the input methods used in that script are simplistic compared to what's available to us.
    # Thank you to the original authors!
    """Step 1: Get a request token. This is a temporary token that is used for
    having the user authorize an access token and to sign the request to obtain
    said access token."""
    session = OAuth1Session(client_key=api_key, client_secret=api_secret)
    try:
        response = session.fetch_request_token(request_token_url)
    except TokenRequestDenied:
        print("Invalid API key/secret provided: {0} / {1}".format(api_key, api_secret))
        sys.exit(1)
    resource_owner_key, resource_owner_secret = (
        response.get("oauth_token"),
        response.get("oauth_token_secret"),
    )
    """Step 2: Redirect to the provider. Since this is a CLI script we do not
    redirect. In a web application you would redirect the user to the URL
    below."""
    user_confirmation_url = "{authorize_url}?oauth_token={oauth_token}&scope={scope}&expiration={expiration}&name={name}".format(
        authorize_url=authorize_url,
        oauth_token=resource_owner_key,
        expiration="never",
        scope="read,write",
        name="PoliCal",
    )
    print(
        "Visite la siguiente URL en su navegador web para autorizar a PoliCal acceso a su cuenta:"
    )
    print("  " + user_confirmation_url)
    print(
        "Concedale los permisos a PoliCal para acceder a sus datos de Trello, estas credenciales se mantendran de manera local"
    )
    input("Presione ENTER para ir al enlace")
    if not no_open:
        with DevNullRedirect():
            webbrowser.open_new_tab(user_confirmation_url)
    """After the user has granted access to you, the consumer, the provider will
    redirect you to whatever URL you have told them to redirect to. You can
    usually define this in the oauth_callback argument as well."""
    confirmation = input("¿Has autorizado a PoliCal? Escriba n para no y S para si:")
    while confirmation == "n":
        confirmation = input(
            "¿Has autorizado a PoliCal? Escriba n para no y S para si:"
        )

    oauth_verifier = input("¿Cuál es el código de verificación?:").strip()
    """Step 3: Once the consumer has redirected the user back to the oauth_callback
    URL you can request the access token the user has approved. You use the
    request token to sign this request. After this is done you throw away the
    request token and use the access token returned. You should store this
    access token somewhere safe, like a database, for future use."""
    session = OAuth1Session(
        client_key=api_key,
        client_secret=api_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=oauth_verifier,
    )
    access_token = session.fetch_access_token(access_token_url)

    """Step 4: Ahora se debe buscar el calendario en formato ICS generado por el
    Aula Virtual"""
    print("\n\n")
    print("PASO 3: Obtención del calendario del Aula Virtual")
    print(
        "Recuerde ingresar e iniciar sesion previamente a https://aulasvirtuales.epn.edu.ec/"
    )
    print(
        "A continuación se abrirá un link hacia el Aula Virtual EPN, en proximos eventos para: elija Todos los cursos"
    )
    print(
        "y a continuación desplácese a la parte más inferior de la página y de clic en el botón Exportar Calendario"
    )
    print(
        'Luego, en la opción Exportar seleccione todos los eventos y después en "para" seleccione los 60 días recientes y próximos'
    )
    print("Finalmente de clic en el boton Obtener URL del calendario")
    print(
        "Visite la siguiente URL en su navegador web para obtener el calendario del aula virtual EPN:"
    )
    print("  " + calendar_moodle_epn_url)
    input(
        "Presione ENTER para ir al enlace e iniciar el proceso, no olvide verificar si su sesión del Aula Virtual se encuentra activa"
    )
    if not no_open:
        with DevNullRedirect():
            webbrowser.open_new_tab(calendar_moodle_epn_url)
    calendar_url = calendar_moodle_epn_url
    while not (configuration.check_for_url(calendar_url)):
        calendar_url = input(
            "Por favor, introduzca el url generado por el Aula Virtual, si este es erróneo se volverá a solicitar:"
        )
    final_output_data = {
        "oauth_token": access_token["oauth_token"],
        "oauth_token_secret": access_token["oauth_token_secret"],
        "api_key": api_key,
        "api_secret": api_secret,
        "calendar_url": calendar_url,
    }
    print("\n\n")
    # Ensure we have a folder to put this in, if it's in a nested config location
    """
    output_folder = os.path.dirname(output_file)
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
        print('Created folder {0} to hold your configuration'.format(output_folder))
    # Try to be safe about not destroying existing credentials
    """
    board_id, owner_id = get_working_board_id(
        api_key,
        api_secret,
        access_token["oauth_token"],
        access_token["oauth_token_secret"],
    )
    final_output_data["board_id"] = board_id
    final_output_data["owner_id"] = owner_id
    if check_file_existence(output_file):
        check_user_on_file(output_file, username + owner_id)
        with open(output_file) as file:
            # use safe_load instead load
            super_final = yaml.safe_load(file)
            super_final[username + owner_id] = final_output_data
            connectSQLite.save_user(username + owner_id)
    else:
        super_final = {username + owner_id: final_output_data}
        connectSQLite.save_user(username + owner_id)
    with open(output_file, "w") as f:
        f.write(yaml.safe_dump(super_final, default_flow_style=False))


def get_working_board_id(
    api_key: str, api_secret: str, oauth_token: str, oauth_token_secret: str
) -> (str, str):
    """This function is for getting the TareasPoli Board ID that is created in the onboard process

    Args:
        api_key (str):  The api key to acceso Trello
        api_secret (str): The api secret to acceso Trello
        oauth_token (str): The oauth token to acceso Trello
        oauth_token_secret (str): The oauth token secret to acceso Trello

    Returns:
        board_id (str): This is the board id of TareasPoli board
        owner_id (str): This is the owner id of Trello user
    """
    client = trello.TrelloClient(
        api_key=api_key,
        api_secret=api_secret,
        token=oauth_token,
        token_secret=oauth_token_secret,
    )
    board_id = ""
    owner_id = ""
    all_boards = client.list_boards()
    for board in all_boards:
        if board.name == "TareasPoli":
            board_id = board.id
    if board_id == "":
        logging.error(('No se encontró el board "TareasPoli", será creado ahora'))
        print('No se encontró el board "TareasPoli", será creado ahora')
        client.add_board("TareasPoli")
        all_boards = client.list_boards()
        for board in all_boards:
            if board.name == "TareasPoli":
                board_id = board.id
    owner_id = board.all_members()[-1].id
    return board_id, owner_id


def check_user_on_file(output_file: str, username: str):
    """This functions checks if an user already exists on yaml file.

    Args:
        output_file (str):  File location
        username (str): The username that would be checked.

    Returns:
        Stop onboard function if the username already exists and the user answers N to overwrite it.
    """
    if os.path.exists(output_file):
        with open(output_file) as file:
            # use safe_load instead load
            users = yaml.safe_load(file)
            if users and username in users.keys():
                overwrite = input(
                    "El nombre de usuario actualmente ya existe, sobreescribir? s/N:"
                )
                if overwrite == "N":
                    return


def check_file_existence(output_file: str) -> bool:
    """This functions checks if the file already exists on filesystem

    Args:
        output_file (str):  File location

    Returns:
        bool.  The return code::

          False -- If the file not exists or is blank
          True -- If already exists
    """
    if os.path.exists(output_file):
        with open(output_file) as file:
            # use safe_load instead load
            users = yaml.safe_load(file)
            if len(users.keys()) > 0:
                return True
            else:
                return False
    else:
        return False


# onboard(True)
