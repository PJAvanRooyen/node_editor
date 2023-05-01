from flask import Flask

app = Flask(__name__)


# NOTE: the class name must be the same as the file name (case insensitive)
class Incrementer:
    def __init__(self):
        self.value = None

    # A function with the Flask route decorator
    @app.route("/hello")
    def hello(self):
        return {"value": "Hello, world!"}


my_instance = Incrementer()