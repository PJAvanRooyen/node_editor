from flask import Flask, Blueprint
import os
import importlib.util

app = Flask(__name__)

scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
scripts = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]

for script in scripts:
    module_name = os.path.splitext(script)[0]
    module_path = os.path.join(scripts_dir, script)

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    blueprint_name = module_name.replace(".", "_")
    blueprint = Blueprint(blueprint_name, __name__)

    for name, cls in module.__dict__.items():
        if isinstance(cls, type) and name.lower() == module_name.lower():
            for method_name, func in cls.__dict__.items():
                if callable(func) and not method_name.startswith("_"):
                    instance = cls()
                    method = getattr(instance, method_name, None)
                    if method is not None:
                        blueprint.add_url_rule(
                            f"/{method_name}",
                            method_name,
                            lambda *args, **kwargs: method(*args, **kwargs),
                            methods=["GET", "POST"]
                        )

    app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run()
