# PoliCal
Los estudiantes de la Escuela Politécnica Nacional(EPN) utilizan una versión de moodle para la administración de tareas, exámenes, etc de ciertas materias en cada semestre, en ciertas ocasiones estos son habilitados sin previo aviso a los estudiantes. El fin de PoliCal es poder sincronizar desde el calendario electrónico que ofrece el aula virtual hacia Trello que es una plataforma muy poderosa para organizar tareas y proyectos.
### Preparar ambiente de python antes de primera ejecución
Antes de la primer ejecución de PoliCal y luego de haber clonado este repositorio es necesario preparar python con la instalación de las librerías necesarias. Para ello será necesario tener:
- Python 3.5 o mayor. (Puedes obtener python aquí: https://www.python.org/downloads/)
- Pip (Puedes obtener pip aquí: https://pip.pypa.io/en/stable/installing/)
- Cuenta en Trello iniciada sesión en el navegador predeterminado. (Puedes registrarte aquí: https://trello.com/signup)
- Cuenta del Aula Virtual EPN iniciada sesión en el navegador predeterminado.

#### Es necesario que su terminal o CMD se este ejecutando en el directorio donde se clonó/descargó el proyecto.

### Para Linux

Con estos requisitos mínimos debe ejecutar este comando en su terminal:
```
pip install -r requeriments.txt
```
Precaución en caso de existir errores en la instalación de los paquetes requeridos, intente agregando **--user** al final del comando.

Luego puede ejecutar polical.py
```
python polical.py
```

### Para Windows

Con estos requisitos mínimos debe ejecutar este comando en CMD.
Si tiene agregado python a los PATH del sistema:
```
python -m pip install -r requeriments.txt
```
Caso contrario:
```
py -m pip install -r requeriments.txt
```
Precaución en caso de existir errores en la instalación de los paquetes requeridos, intente agregando **--user** al final del comando.

Luego puede ejecutar polical.py
Si tiene aregado python a los PATH del sistema:
```
python polical.py
```
Caso contrario:
```
py polical.py
```

### NOTAS
Actualmente se encuentran precargadas todas las materias obtenidas desde el SAEW de las siguientes carreras:
- Ingeniería en Sistemas Informáticos y de Computación PENSUM: 2009B
- Ingeniería Eléctrica PENSUM: 2010
- Ingeniería en Electrónica y Redes de Información PENSUM: 2010
- Ingeniería en Electrónica y Telecomunicaciones PENSUM: 2010
- Ingeniería en Electrónica y Control PENSUM: 2010
- Ingeniería en Mecánica PENSUM: 2009D

Si deseas usar el programa y tu carrera no se encuentra registrada envía un correo luis.andradec14@gmail.com con los horarios de materias sea en PDF o idealmente en EXCEL. 

Lo puedes obtener desde esta página iniciando previamente sesión en el SAEW https://saew.epn.edu.ec/SAEINF/HorariosMaterias.aspx

PoliCal no se encuentra asociado de ninguna forma con Trello.
