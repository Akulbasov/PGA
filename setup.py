from setuptools import setup

setup(name='pga',
      version='0.1',
      description='This is a library for batch CV3 request and extracting data from Google Analytics into Python.',
      url='https://github.com/Akulbasov/PGA',
      author='Artem Kulbasov',
      author_email='kulbasov@agima.ru',
      packages=['pga'],
      install_requires=['google-api-python-client > 1.5.0',
                      'oauth2client==3.0.0',
                      'pandas > 0.13.0','numpy > 1.0.0'], 
     zip_safe=False)
