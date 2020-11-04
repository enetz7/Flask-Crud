"""Click commands."""

from os import remove, walk
from pathlib import Path
from subprocess import call

from click import command, echo, option

from config import ROOT_FOLDER


@command(short_help='Remove *.pyc and *.pyo files recursively.')
def clean():
    types = ('pyc', 'pyo')  # the tuple of file types, @see https://stackoverflow.com/a/4568638
    for root, _, files in walk(ROOT_FOLDER):
        for filename in files:
            if filename.lower().endswith(types):
                path = Path(root).joinpath(filename).__str__()
                echo('Removing \'%s\'' % path.replace(ROOT_FOLDER, '.'))
                remove(path)


@command(short_help='Lint and check code style with \'flake8\' and \'isort\' recursively.')
@option('-f', '--fix-imports', default=False, help='Use \'isort\' to fix imports before linting.',
        is_flag=True)
def lint(fix_imports, skip=['__pycache__', '__pypackages__']):
    directories = [name for name in next(walk(ROOT_FOLDER))[1] if not name.startswith('.')]
    files = [name.__str__() for name in list(Path(ROOT_FOLDER).glob(pattern='*.py'))]
    files_and_directories = [arg for arg in directories + files if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        echo('%s: %s' % (description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'pipx', 'run', '--pypackages', 'isort',
                     '--skip-gitignore')
    return execute_tool('Checking code style', 'pipx', 'run', '--pypackages', 'flake8',
                        '--exclude=.tox', '--max-line-length', '99')
