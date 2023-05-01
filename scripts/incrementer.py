from flask import Flask

app = Flask(__name__)

class Incrementer:
    def __init__(self):
        self.value = None

    # A function with the Flask route decorator
    @app.route("/hello")
    def hello(self):
        return {"value": "Hello, world!"}

my_instance = Incrementer()