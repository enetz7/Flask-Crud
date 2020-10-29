from os import getcwd, getenv, sep
from sys import argv, exit
from threading import Thread

from PyQt5 import QtCore, QtGui, QtWebEngineWidgets, QtWidgets

from config import path

HOST = getenv('FLASK_RUN_HOST', '127.0.0.1')
ICON = '{}{}assets{}images{}logo.svg'.format(getcwd(), sep, sep, sep)
PORT = getenv('FLASK_RUN_PORT', 5000)
PROTOCOL = 'https' if getenv('FLASK_RUN_CERT', None) and getenv('FLASK_RUN_KEY', None) else 'http'
TITLE = path.basename(path.root)


# @see https://github.com/Widdershin/flask-desktop/blob/master/webui/webui.py
class UI:

    def __init__(self, maximized=False):
        self.maximized = maximized
        # create pyqt5 app
        self.qt_app = QtWidgets.QApplication(argv)
        self.qt_app.setApplicationName(TITLE)
        self.qt_app.setWindowIcon(QtGui.QIcon(ICON))
        self.qt_view = QtWebEngineWidgets.QWebEngineView(self.qt_app.activeModalWidget())

    def run(self, app):
        self.thread(app=app).start()
        self.run_ui(url='{}://{}:{}'.format(PROTOCOL, HOST, PORT))

    def run_ui(self, url):
        self.qt_view.load(QtCore.QUrl(url))

        change_setting = self.qt_view.page().settings().setAttribute
        settings = QtWebEngineWidgets.QWebEngineSettings
        change_setting(settings.LocalStorageEnabled, True)
        change_setting(settings.PluginsEnabled, True)
        if self.maximized:
            self.qt_view.showMaximized()
        else:
            self.qt_view.show()

        # start the app
        exit(self.qt_app.exec_())

    @staticmethod
    def thread(app):
        return Thread(target=app.run, daemon=True, kwargs={
            'debug': app.debug,
            'host': HOST,
            'port': PORT,
            'threaded': True,
            'use_reloader': False
        })
