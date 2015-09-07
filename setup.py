from setuptools import setup

setup(
    name='runner',
    version='2.0',
    py_modules=['bin/runner', 'bin/storePass.py'],
    install_requires=['paramiko'],
    bin=['bin/runner', 'bin/storePass.py', 'bin/starttunnel'],
)
