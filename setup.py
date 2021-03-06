import os
import pip
import sys
from setuptools import setup


def parse_requirements():
    """Return abstract requirements (without version numbers)
    from requirements.txt.

    As an exception, requirements that are URLs are used as-is.

    This is tested to be compatible with pip 9.0.1.

    Background: https://stackoverflow.com/a/42033122/
    """

    path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = pip.req.parse_requirements(
        path, session=pip.download.PipSession()
    )
    requirements = [req.name or req.link.url for req in requirements]
    return requirements


install_requires = parse_requirements()

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
