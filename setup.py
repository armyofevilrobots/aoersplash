from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='aoersplash',
      version=version,
      description="",
      long_description="""\
              Generates a page, cleverly, using templates, from a set of RSS
              feeds. Useful for generating static content from a dynamic
              blog to handle large load levels.
              Just a special case little piece of code I wrote for
              http://armyofevilrobots.com/
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      scripts = ['aoersplash/scripts/mksplash',]
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
