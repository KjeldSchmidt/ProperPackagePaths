import properpackagepaths.bar
from properpackagepaths.bar import bar
from properpackagepaths.submodule.baz import baz
from .util import get_project_root_dir

print(get_project_root_dir())


def foo() -> bool:
    return bar()


def bar_module_caller() -> bool:
    return properpackagepaths.bar.bar()


def baz_caller() -> bool():
    return baz()
