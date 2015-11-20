from setuptools import setup, find_packages
import sys, os

version = '0.1'

requires = [
    'eve<0.6',  # https://github.com/RedTurtle/eve-sqlalchemy/issues/79
    'eve-sqlalchemy',
    'pastescript',
    'wsgiutils'
]

setup(name='gmi.most_used_sites.backend',
      version=version,
      description="REST backend for Most used Sites project",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Stefan Walluhn, Arne Winter',
      author_email='stefan@neuland.io',
      url='',
      license='GPLv3',
      packages=['gmi', 'gmi.most_used_sites', 'gmi.most_used_sites.backend'],
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
