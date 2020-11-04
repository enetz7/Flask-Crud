"""A very recommendable tutorial is here:
    https://github.com/mjhea0/flaskr-tdd
"""

if __name__ == '__main__':
    from pathlib import Path
    from sys import exit, path, version

    path.append(Path.cwd().joinpath('__pypackages__', version[:3], 'lib').__str__())
    path.append(Path.cwd().joinpath('src').__str__())

    from pytest import main

    exit(main([Path(__file__).parent.__str__(), '--verbose']))
