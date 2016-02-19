from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys, os

version = '0.9.dev0'

requires = [
    'alembic',
    'colander',
    'cornice',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
]

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(name='gmi.mostusedsites.backend',
      version=version,
      description="REST backend for Most used sites project",
      long_description="""\
REST backend for Most used sites project
========================================

Collects browsing behavior gathered by the Most used sites Firefox Add-On. It
evaluates the data and presents them via a REST API.
""",
      classifiers=[
          'Framework :: Pyramid',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet :: WWW/HTTP :: WSGI'
      ],
      keywords='geyer-moldfusz geyer moldfusz mostusedsites backend rest api',
      author='Stefan Walluhn, Arne Winter',
      author_email='stefan@neuland.io',
      url='https://github.com/geyer-moldfusz/gmi.most_used_sites.backend',
      license='GPLv3',
      packages=['gmi', 'gmi.mostusedsites', 'gmi.mostusedsites.backend'],
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      test_suite='gmi.mostusedsites.backend',
      install_requires=requires,
      tests_require=['tox'],
      cmdclass = {'test': Tox},
      entry_points="""\
      [paste.app_factory]
      main = gmi.mostusedsites.backend:main
      [console_scripts]
      initialize_db = gmi.mostusedsites.backend.scripts.initializedb:main
      """,
      )
