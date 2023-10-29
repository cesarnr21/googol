from setuptools import setup, find_packages
import os, re
from googol import utils
from pathlib import Path

PATH = Path(__file__).parent
LONG_DESCRIPTION = (PATH / 'README.md').read_text(encoding='utf-8')


with open(PATH / 'googol/__init__.py') as file:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read()).group(1)

# TODO: remove these comments
# with open(os.path.join('googol', '__init__.py')) as file:
#     version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read()).group(1)

setup(
    name = 'googol',
    version = version,
    author = 'Cesar Nunez Rodriguez',
    author_email = 'cesarnr21@gmail.com',
    url = 'https://github.com/cesarnr21/googol',
    test_suite='tests',
    # TODO: this line and the long description below.
    # could replace the line below with, packages=find_packages(where='src') and rename the source code folder
    packages = ['googol'],
    description = 'A package to interact with some Google Services',
    # long_description = __doc__,   # use one or the other
    long_description = LONG_DESCRIPTION,
    # FIXME: for some reason installing this package without 
    # installing these dependencies separately results in an error
    install_requires = [
        'google-auth',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'pytest'
    ]
)

# TODO: add a function in `googol.tasks` that allows you to test and set up the json file to save
