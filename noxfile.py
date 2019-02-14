# Copyright 2019 Alix Hamilton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import nox

@nox.session(python='3.6')
def cover(session):
    """Run the final coverage report.
    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install('coverage', 'pytest-cov')
    session.run('coverage', 'report', '--show-missing', '--fail-under=100')
    session.run('coverage', 'erase')


@nox.session(python='3.6')
def lint(session):
    """Run linters.
    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install('flake8')
    session.install('.')
    session.run('flake8', 'nbsampleutils')
    session.run('flake8', 'tests')


@nox.session(python='3.6')
def tests(session):
    # Install py.test
    session.install('pytest')    # Install everything in requirements.txt
    session.install('-r', 'requirements.txt')
    # Install the current package in editable mode.
    session.install('-e', '.')
    # Run py.test. This uses the py.test executable in the virtualenv.
    session.run(
        'py.test',
        '--quiet',
        '--cov=nbsampleutils',
        '--cov=tests',
        '--cov-append',
        '--cov-config=.coveragerc',
        '--cov-report=',
        '--cov-fail-under=97',
        'tests',
    )
