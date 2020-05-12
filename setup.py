import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PoliCalAAL",
    version="1.0.0",
    author="andr3slelouch",
    author_email="luis.andradec14@gmail.com",
    description="Este es un programa hecho en python para sincronizar tareas existentes en el aula virtual de moodle EPN con una cuenta de Trello.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andr3slelouch/PoliCal/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)
