'''
FIXME: add appropiate docstring
'''

from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / 'assets'
TEST_FILES = {file.stem:file for file in sorted(DATA_PATH.iterdir())}
