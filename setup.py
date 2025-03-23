#setting project as local package

from setuptools import find_packages,setup

setup(
    name='GenAI project',
    version='0.0.0',
    author='Sanmesh Desai',
    author_email='sanmeshdesai725@gmail.com',
    packages=find_packages(),
    install_requires=[]
)