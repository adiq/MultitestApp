try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
import os

if sys.argv[-1] == 'test':
    os.system("python manage.py test")
    sys.exit()

setup(
    name='tshapp',
    version='0.1',
    packages=['tshapp', 'multitest', 'multitest_admin'],
    url='http://adiq.eu',
    license='MIT',
    author='Adrian Zmenda',
    author_email='adiq@adiq.eu',
    description='TSH Test Application',
    install_requires=['django==1.6.5', 'django-inplaceedit==1.3.0', 'psycopg2']
)
