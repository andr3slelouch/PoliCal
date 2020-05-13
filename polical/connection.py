import trello
import requests
from polical import configuration
import logging
logging.basicConfig(filename=configuration.get_file_location('Running.log'),level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class GTDException(Exception):
    '''single parameter indicates exit code for the interpreter, because
    this exception typically results in a return of control to the terminal'''

    def __init__(self, errno):
        self.errno = errno

class TrelloConnection:
    '''this one handles connection, retry attempts, stuff like that so it doesn't bail out each
    time we lose connection
    creating a connection requires configuration to be parsed because we need the api keys- so this will need to be invoked
    after the config parser is done doing its thing, with a parameter perhaps being the config

    :param bool autoconnect: should we make a network connection to Trello immediately?
    '''

    def __init__(self, config, autoconnect=True):
        self.autoconnect = autoconnect
        self.config = config
        self.trello = self.__connect(config) if autoconnect else None

    def __connect(self, config):
        trello_client = self.initialize_trello(config)
        try:
            # A simple API call (data reused in BoardTool.get_main_board) to initiate connection & test our credentials etc
            self.boards = trello_client.fetch_json('/members/me/boards/?filter=open')
            return trello_client
        except requests.exceptions.ConnectionError:
            logging.critical('[FATAL] Could not connect to the Trello API!')
            raise GTDException(1)
        except trello.exceptions.Unauthorized:
            logging.critical('[FATAL] Trello API credentials are invalid')
            raise GTDException(1)

    def __repr__(self):
        c = 'disconnected' if self.trello is None else 'connected'
        # isaac: se corrigio: return 'TrelloConnection {0} at {0}'.format(c, id(self))
        return 'TrelloConnection {0} at {1}'.format(c, id(self))

    def __str__(self):
        return repr(self)

    def initialize_trello(self, config):
        '''Initializes our connection to the trello API
        :param dict config: parsed configuration from the yaml file
        :returns: trello.TrelloClient client
        '''
        trello_client = trello.TrelloClient(
            api_key=config.api_key,
            api_secret=config.api_secret,
            token=config.oauth_token,
            token_secret=config.oauth_token_secret,
        )
        return trello_client
