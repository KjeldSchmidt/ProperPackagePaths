import inspect
from properpackagepaths.foo import foo, baz_caller, bar_module_caller
from properpackagepaths.the_real_stuff import get_module_prefix, module_to_module_spec, at
import properpackagepaths
import properpackagepaths.bar
import properpackagepaths.submodule.baz

from unittest import mock

attributes_of_interest = ["__name__", "__package__", "__path__", "__file__", "__spec__"]


def test_add() -> None:
    root_package = module_to_module_spec(properpackagepaths)
    print(get_module_prefix(root_package))
    nested_package = module_to_module_spec(properpackagepaths.submodule)
    print(get_module_prefix(nested_package))
    members = inspect.getmembers(properpackagepaths)
    for name, value in members:
        if name in attributes_of_interest:
            pass
            # print(f"{name} = {value}")
        # print(name)

    assert True


def test_import_function_from_sibling_module():
    result = at(properpackagepaths.foo, properpackagepaths.bar.bar)
    assert result == "properpackagepaths.foo.bar"
    with mock.patch(result, mock.Mock(return_value=True)):
        assert foo() is True


def test_import_function_from_sibling_submodule():
    result = at(properpackagepaths.foo, properpackagepaths.submodule.baz.baz)
    assert result == "properpackagepaths.foo.baz"
    with mock.patch(result, mock.Mock(return_value=True)):
        assert baz_caller() is True


def test_use_function_via_module_import():
    result = at(properpackagepaths.foo, properpackagepaths.submodule.baz.baz)
    assert result == "properpackagepaths.foo.baz"
    with mock.patch(result, mock.Mock(return_value=True)):
        assert baz_caller() is True


def test_use_function_via_qualified_package():
    result = at(properpackagepaths.foo, properpackagepaths.submodule.baz.baz)
    assert result == "properpackagepaths.foo.baz"
    with mock.patch("properpackagepaths.foo.properpackagepaths.bar.bar", mock.Mock(return_value=True)):
        assert bar_module_caller() is True
