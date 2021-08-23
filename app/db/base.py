import importlib
import os

module_path = ["app", "models"]
modules_tree = os.listdir(os.path.abspath(os.path.join(*module_path)))
for module_name in modules_tree:
    if "__" not in module_name:
        module_base_name = module_name.split(".")[0]
        absolute_module_path = ".".join(module_path) + "." + module_base_name
        module = importlib.import_module(absolute_module_path)
