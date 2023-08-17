import inspect
from importlib.machinery import ModuleSpec


def at(target_package, target_function) -> str:
    target_module_spec = module_to_module_spec(target_package)
    print(target_module_spec)
    function_repr = function_to_whatever(target_function)
    return f"{target_module_spec.name}.{function_repr['__name__']}"


def get_module_prefix(module: ModuleSpec) -> str:
    return module.name


def module_to_module_spec(raw_module) -> ModuleSpec:
    members = inspect.getmembers(raw_module)
    for name, value in members:
        if name == "__spec__":
            return value


def function_to_whatever(function):
    interesting_keys = ["__name__"]
    interesting_items = {}
    members = dict(inspect.getmembers(function))
    for name, value in members.items():
        if name in interesting_keys:
            interesting_items[name] = value

    return interesting_items
