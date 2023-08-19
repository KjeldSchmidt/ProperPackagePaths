import inspect
from importlib.machinery import ModuleSpec
from typing import Any, Callable, TypeAlias

Module: TypeAlias = Any
CallTarget = Callable[[], Any]


def at(target_package: Module, target_function: CallTarget) -> str:
    stack = inspect.stack()
    literal_args = extract_literal_call_args(stack)
    target_module_spec = module_to_module_spec(target_package)
    return f"{target_module_spec.name}.{literal_args[1]}"


def get_module_prefix(module: ModuleSpec) -> str:
    return module.name


def extract_literal_call_args(stack: list[inspect.FrameInfo]) -> list[str]:
    context = stack[1].code_context
    assert context is not None
    call = context[0]
    call = call.split("(")[1].strip()
    call = call.split(")")[0].strip()
    literal_args = call.split(",")

    return [arg.strip() for arg in literal_args]


def module_to_module_spec(raw_module: Module) -> ModuleSpec:
    members = inspect.getmembers(raw_module)
    for name, value in members:
        if name == "__spec__":
            spec: ModuleSpec = value
            return spec

    raise Exception("No module was found")


def function_to_whatever(function: CallTarget) -> dict[str, str]:
    interesting_keys = ["__name__", "__module__"]
    interesting_items = {}
    members = dict(inspect.getmembers(function))
    for name, value in members.items():
        if name in interesting_keys:
            interesting_items[name] = value

    return interesting_items
