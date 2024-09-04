from setuptools import setup, find_packages

import os

MODULE_STUB = 'aps1'

def find_subdir(start_dir):
    # Get the list of all subdirectories starting at the given path
    subdirectories = [x[0] for x in os.walk(start_dir)]
    subdirectories = [x.split('/',1)[-1]+'/*' for x in subdirectories]
    return subdirectories

# Adiciona todos os arquivos encontrados ao package_data
setup(
    name="aps1",
    version="0.1.0",
    description="Um jogo estilo Angry Birds no espaço",
    author="Caio Frigerio",
    author_email="caioliberal@gmail.com",
    url="https://github.com/Caiolib/aps1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
    '': find_subdir(f'{MODULE_STUB}/assets'),
    },
    install_requires=[
        "pygame==2.1.0",
        "numpy==1.23.5"
    ],
    entry_points={
        'console_scripts': [
            'aps1=aps1.app:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)

