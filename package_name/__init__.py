"""
Import all definitions under this directory, so you can import as "from <directory name> import <definition name>"
Definitions define interfaces that may be implemented in various ways over time.
Definitions may be any type of Python variable or value: functions, classes, objects, constants, etc.

Since modules may import other modules, only a reference to each definition
file is imported at first and then each module is loaded when first used.
"""
import importlib
import ntpath
import os
import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from os.path import join

import git

space_path = os.path.dirname(__file__)
space_name = os.path.basename(space_path)
reload_defs = os.environ.get("RELOAD_DEFs", False)


def _import_from_path(path: str):
    """Given a filepath, return the module"""
    name = os.path.basename(path).replace(".py", "")
    mod = None
    try:
        spec = spec_from_file_location(name, path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
    except ModuleNotFoundError as e:
        if not str(e).endswith(f" {name}"):
            # Failed import of some other module in the module file
            raise e
    return mod


def _def_from_path(path: str):
    """Return definition function or object at provided path"""
    mod = _import_from_path(path)
    if mod:
        try:
            definition = getattr(mod, mod.__name__)
        except AttributeError:
            return None
    else:
        return None
    return definition


def import_space_defs(space_path, load_defs: bool = True, search_def: str = None):
    """Import all modules in the given directory path and return a dictionary of modules
    keyed by definition name
    if search_def is set, will stop search after finding the provided module name"""
    space_defs = {}
    # Find directories at the space level
    for dirpath, dirs, files in os.walk(space_path):
        dirsplits = dirpath.split(os.sep)
        # For each directory, find the definition file
        for dir_name in dirs:
            if dir_name.startswith("_"):
                # e.g. __pycache__
                continue
            def_filename = join(dirpath, dir_name, dir_name + ".py")
            try:
                if load_defs:
                    # Get function with same name inside module
                    definition = _def_from_path(def_filename)
                else:
                    definition = def_filename
                if definition:
                    space_defs[dir_name] = definition
                if search_def is not None and search_def == dir_name:
                    break
            except FileNotFoundError:
                pass
    return space_defs


class ReloadWrapper(object):
    """If reload_def, execute the function's defining code on every import.
    Otherwise, load only once"""

    def __init__(self, def_filename, space_name, mod_name, reload_def=False):
        """save the file location of the definition to load later"""
        self.def_filename = def_filename
        if not reload_def:
            self.space_name = space_name
            self.mod_name = mod_name
            self.load_definition = self.load_definition_once

    def __call__(self, *args, **kwargs):
        """Load the definition and call it with arguments"""
        try:
            # Once already loaded
            return self._definition(*args, **kwargs)
        except AttributeError as e:
            if hasattr(self, "_definition"):
                # Must be some other error
                raise e
        self._definition = self.load_definition()
        try:
            return self._definition(*args, **kwargs)
        except TypeError as e:
            if self._definition is None:
                print(f"No definition found at {self.def_filename}", file=sys.stderr)
            else:
                raise e

    def load_definition(self):
        """Return loaded definition"""
        definition = _def_from_path(self.def_filename)
        self.call = definition
        return definition

    def load_definition_once(self):
        """since reload_def is false, only load the first time
        and change __call__ to be the loaded function itself.
        """
        definition = _def_from_path(self.def_filename)
        sys.modules[self.space_name].__dict__[self.mod_name] = definition
        sys.modules[f"{self.space_name}.{self.mod_name}"] = definition
        self.call = definition
        return definition

    def help(self):
        """Return information about the definition"""
        return help(self._definition)

    def definition(self):
        if self._definition:
            return self._definition
        return self.load_definition()

    def __getattr__(self, *args, **kwargs):
        try:
            return super().__getattr__(*args, **kwargs)
        except AttributeError:
            return self.definition.__getattr__(*args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        try:
            return super().__setattr__(*args, **kwargs)
        except AttributeError:
            return self.definition.__setattr__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        try:
            return super().__getitem__(*args, **kwargs)
        except AttributeError:
            return self.definition.__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        try:
            return super().__setitem__(*args, **kwargs)
        except AttributeError:
            return self.definition.__setitem__(*args, **kwargs)

    def __str__(self):
        return str(self.definition)

    def __repr__(self):
        return repr(self.definition)


def import_space(space_path, reload_defs=False, wrapper=ReloadWrapper):
    """Under the directory space_path,
        find all modules and attach to sys.modules for importing
    since modules may import other modules that need to be imported first,
        we always find and wrap all modules in ReloadWrapper
        even if reload_defs is False.
    If reload_defs is True, rerun the module's code every time it's imported.
    If reload_defs
    """
    # Get file names of definitions. Don't load them until they're needed.
    space_defs = import_space_defs(space_path, load_defs=False)
    # Create module for space and attach all its definitions to it
    # Also set each definition in sys.modules
    space_name = os.path.basename(space_path)
    space_mod = importlib.import_module(".", package=space_name)
    # space_mod = _import_from_path(space_path)
    if space_mod:  # space folder may be empty
        space_mod.defs = space_defs
        for def_name, def_filename in space_defs.items():
            mod_def = wrapper(
                def_filename,
                space_name=space_name,
                mod_name=def_name,
                reload_def=reload_defs,
            )
            space_mod.__dict__[def_name] = mod_def
            sys.modules[f"{space_name}.{def_name}"] = mod_def
        sys.modules[space_name] = space_mod
        # set space as attribute of current module
        globals()[space_name] = space_mod


wrapper = ReloadWrapper
import_space(space_path, reload_defs, wrapper)
# Note: Deleting the below variables causes problems if importing multiple spaces at once
# using the __init__.py file at the repository root.

try:
    del ReloadWrapper
    del git
    del import_space
    del import_space_defs
    del importlib
    del join
    del ntpath
    del path
    del reload_defs
    del space_name
    del space_path
    del src_init_path
    del types
    del wrapper

    del defs
    del objects
except Exception:
    pass
