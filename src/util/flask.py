
from os import getcwd, getenv, sep

from flask import Flask, render_template,request,flash
from jinja2 import TemplateNotFound
from config import MixinConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util.extensions import bcrypt, db, migrate
from model.user import User
FOLDER = '{}{}static'.format(getcwd(), sep)
STATIC_FOLDER = getenv('STATIC_FOLDER', FOLDER)
TEMPLATE_FOLDER = getenv('TEMPLATE_FOLDER', STATIC_FOLDER)

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static',
            template_folder=TEMPLATE_FOLDER)


def init_app(config_object=MixinConfig):
    """An application factory, as explained here:
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_error_handlers()
    register_extensions()
    register_views()

    if app.debug:
        from flask_debugtoolbar import DebugToolbarExtension

        # from flask_monitoringdashboard import bind as DashboardExtension

        register_commands()
        DebugToolbarExtension(app=app)
        # DashboardExtension(app=app)


def register_commands():
    """Register Click commands."""
    from util.commands import clean, lint, ps_init, ps_load, ps_shell, ps_url, test, urls
    app.cli.add_command(clean)
    app.cli.add_command(lint)
    app.cli.add_command(ps_init)
    app.cli.add_command(ps_load)
    app.cli.add_command(ps_shell)
    app.cli.add_command(ps_url)
    app.cli.add_command(test)
    app.cli.add_command(urls)


def register_error_handlers():
    """Register error handlers."""
    # @see https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
    @app.errorhandler(500)
    def handle_internal(error):
        db.session.rollback()
        return render_template(template_name_or_list='page-500.html',
                               message='Error: %s' % error), 500

    if not app.debug:
        from logging import basicConfig

        from werkzeug.exceptions import BadRequest

        @app.errorhandler(BadRequest)
        def handle_bad_request(error):
            basicConfig()
            return render_template(template_name_or_list='page-500.html',
                                   message='Bad request: %s' % error), 500

        @app.errorhandler(Exception)
        def handle_exception(error):
            basicConfig()
            return render_template(template_name_or_list='page-500.html',
                                   message='Unhandled exception: %s' % error), 500

db.init_app(app)
def register_extensions():
    """Register Flask extensions."""
    # Expose bcrypt methods
    bcrypt.init_app(app)
    # Init database
    #db.init_app(app)
    # Init database migrations
    migrate.init_app(app, db)


def register_views():
    """Register Flask main route (generic routing)."""
    # @see https://github.com/app-generator/jinja-template-volt-dashboard/blob/master/app/views.py
    @app.route(rule='/', defaults={'segment': 'index.html'})
    @app.route(rule='/<path:segment>')
    def index(segment):
        try:
            # Render the html file (if exists) from static/FILE.html
            return render_template(template_name_or_list=segment)

        except TemplateNotFound:
            return render_template(template_name_or_list='page-404.html'), 404

    """Register Flask routes."""
    import util.views
    @app.route(rule='/login')
    def login():
        return render_template('login.html')

    @app.route(rule='/index')
    def index2():
        return 'index'

    @app.route(rule='/logout')
    def logout():
        return 'logout'
    @app.route(rule='/login', methods=['GET', 'POST'])
    def login_post():
            usernameForm=request.form.get("username")
            passwordForm=request.form.get("password") 
            session = sessionmaker(bind=create_engine(app.config.get('SQLALCHEMY_DATABASE_URI')))
            s = session()
            query = s.query(User).filter(User.username==usernameForm)
            result = query.first()
            if(result and result.check_password(passwordForm)):
                return "ole"
            else:
                return "no ole"
            return render_template('login.html')

