from setuptools import setup, find_packages

setup(
    name="aps1",
    version="0.1.0",
    description="Um jogo estilo Angry Birds no espaço",
    author="Caio Frigerio",
    author_email="caioliberal@gmail.com",
    url="https://github.com/Caiolib/aps1",
    packages=find_packages(),
    include_package_data=True,
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
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.7',
)
