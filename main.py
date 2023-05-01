import subprocess
import threading

from src.node_editor_view.node_editor import NodeEditorApp


def start_app():
    app = NodeEditorApp()
    app.run()


if __name__ == '__main__':
    api_process = subprocess.Popen(['python', 'api.py'])

    thread = threading.Thread(target=start_app())
    thread.start()

    api_process.terminate()