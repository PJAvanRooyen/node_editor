import os
import sys

import requests
import subprocess

# Add the parent directory of the current file to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.node_viewer.node_view import NodeEditorApp

if __name__ == '__main__':
    # Start Flask API as a subprocess
    scripts_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
    script_path = os.path.join(scripts_dir_path, 'increment.py')
    flask_process = subprocess.Popen(['python', script_path])


    app = NodeEditorApp()
    app.run()

    # Stop Flask API
    flask_process.terminate()