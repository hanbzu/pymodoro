try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='pymodoro',
    version='1.0',
    author='Hibai Unzueta',
    author_email='@hanbzu',
    url='',
    py_modules=['pymodoro'],
    entry_points={
        'console_scripts': [
            't = t:_main',
        ],
    },
)