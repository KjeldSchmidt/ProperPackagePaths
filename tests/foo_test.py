from unittest import mock

import fake_code_for_tests.sibling_import
from fake_code_for_tests.mock_target import (
    instance_method_caller,
    sibling_function_import_caller,
    sibling_module_import_caller,
    submodule_function_import_caller,
)
from fake_code_for_tests.sibling_import import Sibling, bar
from fake_code_for_tests.submodule.submodule_import import baz
from properpackagepaths.the_real_stuff import at


def test_import_function_from_sibling_module() -> None:
    result = at(fake_code_for_tests.mock_target, bar)
    with mock.patch(result, mock.Mock(return_value=True)):
        assert sibling_function_import_caller() is True


def test_at_is_formatting_independent() -> None:
    result = at(
        fake_code_for_tests.mock_target, bar  # Long comment to preserve the line break
    )
    with mock.patch(result, mock.Mock(return_value=True)):
        assert sibling_function_import_caller() is True


def test_import_function_from_sibling_submodule() -> None:
    result = at(fake_code_for_tests.mock_target, baz)
    with mock.patch(result, mock.Mock(return_value=True)):
        assert submodule_function_import_caller() is True


def test_use_function_via_qualified_package() -> None:
    result = at(fake_code_for_tests.mock_target, fake_code_for_tests.sibling_import.bar)

    with mock.patch(result, mock.Mock(return_value=True)):
        assert sibling_module_import_caller() is True


def test_call_instance_method() -> None:
    result = at(
        fake_code_for_tests.mock_target,
        Sibling.passes_test,
    )
    assert result == "fake_code_for_tests.mock_target.Sibling.passes_test"
    with mock.patch(
        result,
        mock.Mock(return_value=True),
    ):
        assert instance_method_caller() is True
