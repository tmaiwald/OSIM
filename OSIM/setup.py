from distutils.core import setup
import OSIM

setup(
    name='OSIM',
    description=OSIM.__doc__.splitlines()[0],
    author='Tim Maiwald',
    author_email='tim.maiwald92@googlemail.com',
    py_modules=['OSIM'],
)
