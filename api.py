from flask import Flask, Blueprint, request
import os
import importlib

app = Flask(__name__)
scripts_bp = Blueprint('scripts', __name__)

scripts_dir = 'scripts'

# iterate over files in the scripts directory
for filename in os.listdir(scripts_dir):
    if filename.endswith('.py'):
        # import the module
        module_name = filename[:-3]
        module = importlib.import_module(f'{scripts_dir}.{module_name}')

        # create an instance of the class
        if hasattr(module, 'my_instance'):
            instance = module.my_instance
            print('Instance found')
        else:
            instance = None

        # get the methods from the instance
        if instance:
            get_method = getattr(instance, 'get', None)
            set_method = getattr(instance, 'set', None)

            # add them as endpoints to the blueprint
            if get_method:
                @scripts_bp.route(f'/{module_name}/get')
                def get_endpoint():
                    return get_method()

            if set_method:
                @scripts_bp.route(f'/{module_name}/set', methods=['POST'])
                def set_endpoint():
                    data = request.get_json()
                    value = data.get('value', None)
                    if value is not None:
                        return set_method(value)
                    else:
                        return {'error': 'No value provided.'}

# register the blueprint with the app
app.register_blueprint(scripts_bp, url_prefix='/api')

# start the app
if __name__ == '__main__':
    app.run()
