"""Click commands."""

from os import remove, walk

from click import command, echo, option
from flask import current_app
from flask.cli import with_appcontext

from config import path
from util.database import db, load_fixtures, load_models


def ps_data():
    return current_app.config.get('SQLALCHEMY_DATA')


# @see https://github.com/gothinkster/flask-realworld-example-app/blob/master/conduit/commands.py
@command(short_help='Remove *.pyc and *.pyo files recursively.')
def clean():
    for dirpath, _, filenames in walk(path.root):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                pathname = path.join(dirpath, filename)
                echo('Removing {}'.format(pathname))
                remove(pathname)


@command(short_help='Lint and check code style with \'flake8\' and \'isort\' recursively.')
@option('-f', '--fix-imports', default=False,
        help='Fix imports before linting using \'isort\'.', is_flag=True)
def lint(fix_imports, skip=['__pycache__', '__pypackages__', 'assets', 'requirements', 'static']):
    from subprocess import call

    from util.mixin import glob

    directories = [name for name in next(walk(path.root))[1] if not name.startswith('.')]
    files = glob()
    files_and_directories = [arg for arg in directories + files if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'pipx', 'run', '--pypackages', 'isort',
                     '--skip-gitignore')
    execute_tool('Checking code style', 'pipx', 'run', '--pypackages', 'flake8',
                 '--exclude=.tox', '--max-line-length', '99')


@command(short_help='Create postgres database structure.')
@option('-f', '--fixtures', default=False,
        help='Load initial data into postgres database structure.', is_flag=True)
@with_appcontext  # @see https://stackoverflow.com/a/46541219
def ps_init(fixtures):
    echo('Creating tables for `%s@%s`' % (ps_data()['user'], ps_data()['db']))
    load_models()  # @see https://stackoverflow.com/a/20749534
    db.create_all()
    if fixtures:
        load_fixtures()
    return db.session.commit()


@command(short_help='Load initial data into postgres database structure.')
@with_appcontext
def ps_load():
    load_fixtures()
    return db.session.commit()


@command(short_help='Login the postgres shell, \'psql\' needs to be installed.')
@with_appcontext
def ps_shell():
    from os import environ, system
    environ['PGPASSWORD'] = ps_data()['pw']
    return system('psql -d {db} -U {user} -h {host} -p {port}'.format(**ps_data()))


@command(short_help='Show postgres database connection string.')
@with_appcontext
def ps_url():
    return echo(current_app.config.get('SQLALCHEMY_DATABASE_URI'))


@command(short_help='Run the tests.')
def test():
    from pytest import main
    rv = main([path.test, '--verbose'])
    exit(rv)


@command(short_help='Map the urls, the endpoints with its methods and its rules.')
@with_appcontext
def urls():
    return echo(current_app.url_map)
