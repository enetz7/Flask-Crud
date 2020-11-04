
from flask import current_app

from controller.main import start, stop, svg

"""Add main route (generic routing)."""
# @see https://github.com/app-generator/jinja-template-volt-dashboard/blob/master/app/views.py
current_app.add_url_rule(rule='/', defaults={'segment': 'index.html'}, endpoint='start_default',
                         methods=['GET', 'POST'], view_func=start)
current_app.add_url_rule(rule='/<path:segment>', endpoint='start', methods=['GET', 'POST'],
                         view_func=start)

"""Add shutdown route."""
current_app.add_url_rule(rule='/shutdown', endpoint='stop', methods=['POST'], view_func=stop)

"""Add another route."""
current_app.add_url_rule(rule='/svg', endpoint='svg_default', view_func=svg)
current_app.add_url_rule(rule='/svg/<path:src>', endpoint='svg', view_func=svg)
