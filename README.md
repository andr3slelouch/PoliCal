# PoliCal

Los estudiantes de la Escuela Politécnica Nacional(EPN) utilizan una versión de moodle para la administración de tareas, exámenes, etc de ciertas materias en cada semestre.
El fin de PoliCal es poder sincronizar desde el calendario electrónico que ofrece el aula virtual hacia Trello que es una plataforma muy poderosa para organizar tareas y proyectos.
## Para Linux
### Instalar desde Pypi

Para instalar este programa puede hacerlo accediendo desde Pypi.
```
pip install polical
```
Precaución en caso de existir errores en la instalación de los paquetes requeridos, intente agregando **--user** al final del comando.

Luego puede ejecutar polical.py
```
python -m polical
```
### Instalar desde GitHub

Para instalar este programa desde github debe ejecutar lo siguiente.
```
git clone https://github.com/andr3slelouch/PoliCal.git
cd PoliCal
python setup.py install
```
Luego puede ejecutar polical.py
```
python -m polical
```
## Para Windows
### Instalar desde Pypi
Para instalar este programa puede hacerlo accediendo desde Pypi.
```
python -m pip install polical
```
Caso contrario:
```
py -m pip install polical
```
Precaución en caso de existir errores en la instalación de los paquetes requeridos, intente agregando **--user** al final del comando.

Luego puede ejecutar polical.py
Si tiene aregado python a los PATH del sistema:
```
python -m polical
```
Caso contrario:
```
py -m polical
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
