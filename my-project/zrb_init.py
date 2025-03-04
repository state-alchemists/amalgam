from zrb import load_file
import os

_DIR = os.path.dirname(__file__)
# Load myapp automation
myapp = load_file(os.path.join(_DIR, "myapp", "_zrb", "task.py"))
assert myapp