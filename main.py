import os
import subprocess

from src.node_editor_view.node_editor import NodeEditorApp


if __name__ == '__main__':
    # Start Flask API as a subprocess
    api_dir_path = os.path.join(os.path.dirname(__file__), 'scripts')
    api_path = os.path.join(api_dir_path, 'api.py')
    flask_api = subprocess.Popen(['python', api_path])
    print("Flask subprocess PID:", flask_api.pid)

    app = NodeEditorApp()
    app.run()

    # Stop Flask API
    flask_api.terminate()