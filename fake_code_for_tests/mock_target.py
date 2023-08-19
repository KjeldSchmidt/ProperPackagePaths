import fake_code_for_tests.sibling_import
from fake_code_for_tests.sibling_import import bar
from fake_code_for_tests.submodule.submodule_import import baz


def sibling_function_import_caller() -> bool:
    return bar()


def sibling_module_import_caller() -> bool:
    return fake_code_for_tests.sibling_import.bar()


def submodule_function_import_caller() -> bool:
    return baz()
