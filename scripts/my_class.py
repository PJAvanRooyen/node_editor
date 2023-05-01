from flask import jsonify

class MyClass:
    def __init__(self):
        self.value = 0

    def get(self):
        return {'value': self.value}

    def set(self, value):
        self.value = value
        return {'value': self.value}

my_instance = MyClass()