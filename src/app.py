
"""Create an application instance or show a QWebEngineView.
    A very recommendable read is here:
        https://hackingandslacking.com/demystifying-flasks-application-context-c7bd31a53817
"""


def load_app(config_object=None):
    if __name__ == '__main__':  # @see https://stackoverflow.com/a/56999264
        from pathlib import Path
        from sys import path, version
        path.append(Path.cwd().joinpath('__pypackages__', version[:3], 'lib').__str__())

    from util.flask import app, init_app
    init_app(config_object=config_object)

    if __name__ == '__main__':
        from util.ui import UI
        UI().run(app=app)
    else:
        return app


if __name__ == '__main__':
    from os import getenv
    if not getenv(key='FLASK_SKIP_DOTENV'):
        from dotenv import load_dotenv
        load_dotenv()
    load_app()
else:
    app = load_app()
