"""Python CLI for Microsoft SQL."""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
import sys

from os import path

from setuptools import find_packages, setup
from setuptools.command.test import test

from sql_json_bridge import __version__

here = path.abspath(path.dirname(__file__))


class Tox(test):
    """TestCommand to run ``tox`` via setup.py."""

    def finalize_options(self):
        """Finalize options from args."""
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Actually Run Tests."""
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


def read(*filenames, **kwargs):
    """
    Read file contents into string.
    Used by setup.py to concatenate long_description.
    :param string filenames: Files to be read and concatenated.
    :rtype: string
    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        if path.splitext(filename)[1] == ".md":
            try:
                import pypandoc
                buf.append(pypandoc.convert_file(filename, 'rst'))
                continue
            except:
                with io.open(filename, encoding=encoding) as f:
                    buf.append(f.read())
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


setup(
    name='sql_json_bridge',
    version=__version__,
    description=(' [WIP] modular bridge for accessing SQL style databases via HTTP(JSON).'),
    # long_description=read("README.md", "CONTRIBUTING.md", "CHANGELOG.rst"),

    # The project's main homepage.
    url='https://github.com/rtrox/sql_json_bridge',

    # Author details
    author='Russell Troxel',
    author_email='russelltroxel@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 1 - Planning',

        'Intended Audience :: System Administrators',

        'Topic :: Database :: Front-Ends',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords=['sql', 'mssql', 'mysql'],

    packages=find_packages(),

    install_requires=[
        'flask',
        'PyYAML',
        'stevedore'
    ],
    tests_require=['tox', 'virtualenv'],
    cmdclass={'test': Tox},

    entry_points={
        'sql_json_bridge.ext.database_driver': [
            'mysql = sql_json_bridge.db_drivers.pymysql_driver:MySQLDriver',
            'mssql = sql_json_bridge.db_drivers.pymssql_driver:MSSQLDriver',
        ],
    },
)
