
from os import getenv, sep
from pathlib import Path

from flask import current_app, flash, render_template, request, send_from_directory, session
from jinja2 import TemplateNotFound

from config import ROOT_FOLDER

defaults = {'title': current_app.config.get('TITLE')}


def skin():
    """Invert theme defaults if requested or choose dark by default."""
    skins = ['dark', 'light']
    if request.method == 'POST' and request.form.get('toggle'):
        skins.remove(request.form.get('toggle'))
        session['theme'] = skins[0]
        flash(u'Enjoy %s theme ッ' % skins[0], 'info')

    defaults['theme'] = session['theme'] if 'theme' in session else skins[0]


def start(segment):
    """Render the html file from static/FILE if exists or render static/page-404.html"""
    skin()
    try:
        return render_template(template_name_or_list=segment, **defaults)

    except TemplateNotFound:
        return render_template(template_name_or_list='page-404.html', **defaults), 404


def stop():
    """Stop the werkzeug server."""
    if 'werkzeug.server.shutdown' not in request.environ:

        raise RuntimeError('Werkzeug server is not running.')
    request.environ.get('werkzeug.server.shutdown')()

    return 'Server shutting down...'


def svg(src=None):
    """Render SVG image from '~/Downloads/FILE' or render the favicon by default."""
    home = getenv(key='HOME') + sep + 'Downloads' if getenv(key='HOME') else ROOT_FOLDER
    default = current_app.config.get('ICON')
    directory = Path(home + sep + src).parent.__str__() if src else Path(default).parent.__str__()
    filename = Path(src if src else default).name

    return send_from_directory(directory=directory, filename=filename, mimetype='image/svg+xml')
