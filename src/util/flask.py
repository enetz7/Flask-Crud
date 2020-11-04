"""An application factory, as explained here:
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories
"""

from logging import StreamHandler, basicConfig
from sys import stdout
from jinja2 import TemplateNotFound
from flask import Flask, flash, render_template,request
from flask.cli import AppGroup
from flask.helpers import get_debug_flag
from werkzeug.exceptions import BadRequest

from command.db import ps_init, ps_load, ps_migrate, ps_shell, ps_url
from command.main import clean, lint
from config import STATIC_FOLDER, TEMPLATE_FOLDER, MixinConfig, StageConfig, files, import_file
from model.user import User
from util.extensions import bcrypt, db, login_manager, migrate

app = Flask(import_name=__name__, static_folder=STATIC_FOLDER, static_url_path='/static',
            template_folder=TEMPLATE_FOLDER)


def init_app(config_object=None):
    """Part of the work is based on these files:
        https://flask.palletsprojects.com/en/1.1.x/appcontext/#manually-push-a-context
        https://github.com/gothinkster/flask-realworld-example-app/blob/master/autoapp.py
        https://github.com/gothinkster/flask-realworld-example-app/blob/master/conduit/commands.py

    :param config_object: The configuration object to use.
    """
    # @see https://stackoverflow.com/a/63087331
    ps_cli = AppGroup(help='Perform postgres operations.', name='postgres')
    app.cli.add_command(cmd=ps_cli, name='ps')

    if not config_object:
        config_object = StageConfig if get_debug_flag() else MixinConfig
    app.config.from_object(obj=config_object)
    app.url_map.strict_slashes = False
    register_commands(ps_cli)
    register_error_handlers()
    register_extensions()

    with app.app_context():
        """Register routes."""
        print('Loading routes...')
        for file in files(src='view'):
            import_file(src=file, verbose=True)

    if app.debug:
        """Register development commands."""
        app.cli.add_command(cmd=clean)
        app.cli.add_command(cmd=lint)

    if not app.logger.handlers:
        """Configure logger."""
        app.logger.addHandler(hdlr=StreamHandler(stream=stdout))

    @login_manager.user_loader
    def load(userid):
        """Configure a callback to reload the user object."""
        return User.get_by_id(record_id=userid)


def register_commands(ps_cli):
    """Register production commands."""
    ps_cli.add_command(cmd=ps_init, name='init')
    ps_cli.add_command(cmd=ps_load, name='load')
    ps_cli.add_command(cmd=ps_migrate, name='migrate')
    ps_cli.add_command(cmd=ps_shell, name='shell')
    ps_cli.add_command(cmd=ps_url, name='url')


def register_error_handlers():
    """Register error handlers."""
    # @see https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
    @app.errorhandler(500)
    def handle_internal(error):
        db.session.rollback()
        flash(u'Error: %s' % error, 'error')
        return render_template(template_name_or_list='page-500.html'), 500

    if not app.debug:
        @app.errorhandler(BadRequest)
        def handle_bad_request(error):
            basicConfig()
            flash(u'Bad request: %s' % error, 'error')
            return render_template(template_name_or_list='page-500.html'), 500

        @app.errorhandler(Exception)
        def handle_exception(error):
            basicConfig()
            flash(u'Unhandled exception: %s' % error, 'error')
            return render_template(template_name_or_list='page-500.html'), 500


def register_extensions():
    """Register Flask extensions."""
    # Expose bcrypt methods
    bcrypt.init_app(app=app)
    # Init database
    db.init_app(app=app)
    # Init login manager
    login_manager.init_app(app=app)
    # Init database migrations
    migrate.init_app(app=app, db=db, directory=None)
