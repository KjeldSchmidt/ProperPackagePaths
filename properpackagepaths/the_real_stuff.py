import inspect
from importlib.machinery import ModuleSpec
from typing import Any, TypeAlias

Module: TypeAlias = Any
CallTarget = Any


def at(target_package: Module, target_function: CallTarget) -> str:
    stack = inspect.stack()
    literal_args = extract_literal_call_args(stack)
    target_module_spec = module_to_module_spec(target_package)
    return f"{target_module_spec.name}.{literal_args[1]}"


def get_module_prefix(module: ModuleSpec) -> str:
    return module.name


def extract_literal_call_args(stack: list[inspect.FrameInfo]) -> list[str]:
    frame = stack[1].frame
    calling_line = stack[1].lineno
    source_lines_code, source_start_line = inspect.getsourcelines(frame)
    caller_line_offset = calling_line - source_start_line

    function_call_lines = []
    for line_idx in range(caller_line_offset, len(source_lines_code)):
        original_line = source_lines_code[line_idx]
        code_only = original_line.split("#")[0].strip()  # Remove comments and whitespace
        function_call_lines.append(code_only)
        if code_only.endswith(")"):
            # We are looking for the close-paren on the `at`-call
            # A more robust design would look for balanced parenthesis counts
            # And discard parenthesis in strings
            # But I don't think either one is relevant here right now
            break

    call = " ".join(function_call_lines)
    call = call.split("(")[1].strip()
    call = call.split(")")[0].strip()
    literal_args = call.split(",")
    literal_args = [arg.strip() for arg in literal_args]
    return literal_args


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
