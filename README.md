## PoliCal
Los estudiantes de la Escuela Politécnica Nacional(EPN) utilizan ua versión de moodle para la administración de tareas, exámenes, etc de ciertas materias en cada semestre, en ciertas ocasiones estos son habilitados sin previo aviso a los estudiantes. El fin de PoliCal es poder sincronizar desde el calendario electrónico que ofrece el aula virtual hacia Trello que es una plataforma muy poderosa para organizar tareas y proyectos.
### Preparar ambiente de python antes de primera ejecución
Antes de la primer ejecución de PoliCal y luego de haber clonado este repositorio es necesario preparar python con la instalación de las librerías necesarias. Para ello será necesario tener:
- Python 3.5 o mayor.
- Pip
- Cuenta en Trello iniciada sesión en el navegador predeterminado.
- Cuenta del Aula Virtual EPN iniciada sesión en el navegador predeterminado.

### Para Linux

Con estos requisitos mínimos debe ejecutar este comando en su terminal
```
pip install -r requeriments.txt
```
Es necesario que su terminal se este ejecutando en el directorio donde se clonó el repositorio.

Luego puede ejecutar polical.py
```
python polical.py
```

### Para Windows

Con estos requisitos mínimos debe ejecutar este comando en CMD
Si tiene aregado python a los PATH del sistema:
```
python -m pip install -r requeriments.txt
```
Caso contrario:
```
py -m pip install -r requeriments.txt
```

Es necesario que el CMD se este ejecutando en el directorio donde se clonó el repositorio.

Luego puede ejecutar polical.py
Si tiene aregado python a los PATH del sistema:
```
python polical.py
```
Caso contrario:
```
py polical.py
```
