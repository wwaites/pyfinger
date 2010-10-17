from setuptools import setup, find_packages
import sys, os

version = '0.1'

def readme():
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, "README.txt")
    return open(filename).read()

setup(name='pyfinger',
      version=version,
      description="Python finger program",
      long_description=readme(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='William Waites',
      author_email='ww@styx.org',
      url='http://packages.python.org/pyfinger',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
          [console_scripts]
          pyfinger=pyfinger.command:finger
      """,
      )
