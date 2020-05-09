from setuptools import setup, find_packages


with open('requirements.txt') as file_req:
    install_requires = file_req.read()


setup(
    name='graph_creation',
    version='2.0',
    packages=find_packages(),
    install_requires=install_requires
)
