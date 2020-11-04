"""Database related click commands."""

from os import environ
from subprocess import run

from alembic.command import upgrade
from click import command, echo, option
from flask import current_app
from flask.cli import with_appcontext
from flask_migrate import Migrate

from config import files, import_file
from util.database import db, load_fixtures


def ps_data():
    return current_app.config.get('SQLALCHEMY_DATA')


@command(short_help='Create database structure.')
@option('-f', '--fixtures', default=False, help='Load initial data into database structure.',
        is_flag=True)
@with_appcontext
def ps_init(fixtures):
    """Initialize the database."""
    echo('Creating tables for `%s@%s`' % (ps_data()['user'], ps_data()['db']))
    print('Loading models...')
    for file in files(src='model'):
        import_file(src=file, verbose=True)
    db.create_all()
    if fixtures:
        load_fixtures()
    return db.session.commit()


@command(short_help='Load initial data into database structure.')
@with_appcontext
def ps_load():
    """Load initial data to the database."""
    load_fixtures()
    return db.session.commit()


@command(short_help='Apply migrations into database structure.')
@with_appcontext  # @see https://stackoverflow.com/a/46541219
def ps_migrate():
    """Apply migrations to the database with alembic."""
    config = Migrate(current_app, db).get_config()
    upgrade(config, 'head')


@command(short_help='Login into database shell, \'psql\' needs to be installed.')
@with_appcontext
def ps_shell():
    """Login into database shell."""
    environ['PGPASSWORD'] = ps_data()['pw']
    return exit(run('psql -d {db} -U {user} -h {host} -p {port}'.format(**ps_data())))


@command(short_help='Show database connection string.')
@with_appcontext
def ps_url():
    """Show database connection string."""
    return echo(current_app.config.get('SQLALCHEMY_DATABASE_URI'))
