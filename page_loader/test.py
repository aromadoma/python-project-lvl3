import tempfile
import os


with tempfile.TemporaryDirectory() as td:
    print(f'dir {td} is created')
