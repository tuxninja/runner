from setuptools import setup

setup(
    name='runner',
    version='1.0',
    py_modules=['scripts/runner', 'scripts/prunner'],
    install_requires=['paramiko'],
    scripts=['scripts/runner', 'scripts/prunner'],
)
