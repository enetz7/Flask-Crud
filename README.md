# flask-desktop

A Python module that allows you to convert Flask apps into cross platform desktop apps with three lines of code.

## Installation:

    pip install git+git://github.com/mmozos/flask-desktop.git

I'd like to have flask-desktop available on pip, but currently don't have the time and headspace to make that happen. If you want this to happen, please do it and I'll add you as a collaborator to this repo.

## Usage:

    from util.ui import UI # Add WebUI to your imports
    from flask import Flask, render_template, request

    app = Flask(__name__)

    # all of your standard flask logic

    if __name__ == '__main__':
        UI().run(app) # replace app.run() with UI().run(app), and that's it

flask-desktop is powered by PyQt5, and should run on Windows, Mac and Linux. You can even create standalone executables using PyInstaller!

## License

flask-desktop is licensed under the MIT License. See the LICENSE file for more details.
