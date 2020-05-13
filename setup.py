import setuptools
from polical import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polical",
    version=__version__,
    author="Andrés Andrade",
    author_email="luis.andradec14@gmail.com",
    description="Este es un programa hecho en python para sincronizar tareas existentes en el aula virtual de moodle EPN con una cuenta de Trello.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD-3',
    url="https://github.com/andr3slelouch/PoliCal/",
    packages=setuptools.find_packages(),
    install_requires=[
    'certifi',
    'chardet',
    'idna',
    'oauthlib',
    'py-trello',
    'python-dateutil',
    'pytz',
    'PyYAML',
    'requests',
    'requests-oauthlib',
    'six',
    'urllib3',
    'wget'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Environment :: Console"
    ],
    python_requires='>=3.5',
)
