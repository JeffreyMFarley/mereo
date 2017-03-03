import sys
from setuptools import setup

install_requires = ['svgwrite', 'configargparse']

if sys.version < '3.0':
    install_requires.append('mock')

setup(name='mereo',
      version='0.1',
      description='Tools for manipulating my SVG characters',
      url='https://github.com/JeffreyMFarley/mereo',
      author='Jeffrey M Farley',
      author_email='JeffreyMFarley@users.noreply.github.com',
      license='MIT',
      packages=['mereo'],
      install_requires=install_requires,
      test_suite='tests',
      tests_require=['nose', 'nose_parameterized'],
      zip_safe=False)
