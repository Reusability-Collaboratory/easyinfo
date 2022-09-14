""" Command line utility for repository """
import fire
from repo_utils import get_repository_path
import os
import importlib

# This will make available all definitions found under the same package that this file is found.
# This allows making a command line out of any package with the repo_utils template by putting start_command_line inside it.
package_name = __file__.replace(get_repository_path(), '').split(os.sep)[1]
mod = importlib.import_module(package_name)

def start_command_line():
    """
    Command-line interface for the repository.
    Specify the definition to execute and then any arguments.
    e.g. "define <name>".
    The Fire library converts the specified function or object into a command-line utility.
    """
    global mod
    fire.Fire(mod)
