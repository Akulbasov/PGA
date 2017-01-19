from setuptools import setup
from distutils.core import setup

setup(
    name = 'PGA',
    version = '1',
    description = 'This is a library for batch request and extracting data from Google Analytics into Python.',
    author = 'Artem Kulbasov',
    author_email = 'kulbasov@agima.ru',
    url = 'https://github.com/Akulbasov/PGA/tree/master',
    py_modules=['PGA'],
    install_requires=['google-api-python-client > 1.5.0',
                      'oauth2client',
                      'pandas > 0','numpy > 1'],
)
