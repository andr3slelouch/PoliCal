# PoliCal

Los estudiantes de la Escuela Politécnica Nacional(EPN) utilizan una versión de moodle para la administración de tareas, exámenes, etc de ciertas materias en cada semestre.
El fin de PoliCal es poder sincronizar desde el calendario electrónico que ofrece el aula virtual hacia Trello que es una plataforma muy poderosa para organizar tareas y proyectos.
Actualmente se ha implementado un bot en Telegram, para poder administrar las tareas desde dicha plataforma de mensajería y puede ser utilizado buscando al usuario https://telegram.me/polical_bot
## Para Linux
### Instalar desde Pypi

1. Para instalar este programa puede hacerlo accediendo desde Pypi.
```
pip install polical
```
Precaución en caso de existir errores en la instalación de los paquetes requeridos, intente agregando **--user** al final del comando.

2. Luego puede ejecutar polical.py
```
python -m polical
```
### Instalar desde GitHub

1. Para instalar este programa desde github debe ejecutar lo siguiente.
```
git clone https://github.com/andr3slelouch/PoliCal.git
cd PoliCal
python setup.py install
```
2. Luego puede ejecutar polical.py
```
python -m polical
```
## Para Windows
### Instalar desde Pypi
1. Para instalar este programa puede hacerlo accediendo desde Pypi, si tiene agregado python a los PATH del sistema:.
```
python -m pip install polical
```
Caso contrario:
```
py -m pip install polical
```
Precaución en caso de existir errores en la instalación de los paquetes requeridos, intente agregando **--user** al final del comando.

2. Luego puede ejecutar polical.py
Si tiene agregado python a los PATH del sistema:
```
python -m polical
```
Caso contrario:
```
py -m polical
```

## Opciones disponibles en Línea de Comandos

```
[andr3slelouch]$ polical -h
usage: cli.py [-h] [--add_user] [--todo] [--bot] [--load_subjects_from_csv] [--update_subjects_from_csv] [--show_directory]
              [--set_telegram_token SET_TELEGRAM_TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  --add_user, -au       Add a new user with interactive cli
  --todo, -t            Look for tasks adn write to todo.txt and done.txt
  --bot, -b             Executes the bot for telegram it requires a mysql database executing and a token for Telegram Bot
  --load_subjects_from_csv, -lcsv
                        Load new subjects to the sqlite3 database from materias.csv located in working directory
  --update_subjects_from_csv, -ucsv
                        Updates subjects to the sqlite3 database from materias.csv located in working directory
  --show_directory, -sd
                        Prints the working directory address where the config files are saved
  --set_telegram_token SET_TELEGRAM_TOKEN, -tk SET_TELEGRAM_TOKEN
                        Save the telegram token to config.yaml configuration file
```

## Documentación
Todo el código seencuentra documentado con docstrings y un resumen general puede ser encontrado en [readthedocs](https://polical.readthedocs.io/)

### NOTAS
Actualmente se encuentran precargadas todas las materias obtenidas desde el SAEW de las siguientes carreras:
- Ingeniería en Sistemas Informáticos y de Computación PENSUM: 2009B
- Ingeniería en Computación PENSUM: 2015-ICCR162101
- Ingeniería Eléctrica PENSUM: 2010
- Ingeniería en Electrónica y Redes de Información PENSUM: 2010
- Ingeniería en Electrónica y Telecomunicaciones PENSUM: 2010
- Ingeniería en Electrónica y Control PENSUM: 2010
- Ingeniería en Mecánica PENSUM: 2009D

Si deseas usar el programa y tu carrera no se encuentra registrada, siéntete libre de agregar un nuevo [issue](https://github.com/andr3slelouch/PoliCal/issues/new) con los horarios de materias sea en PDF o idealmente en EXCEL.

Lo puedes obtener desde esta página iniciando previamente sesión en el SAEW https://saew.epn.edu.ec/SAEINF/HorariosMaterias.aspx

PoliCal no se encuentra asociado de ninguna forma con Trello, Telegram, o la Ecuela Politécnica Nacional.
