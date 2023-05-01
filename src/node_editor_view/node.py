from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.network.urlrequest import UrlRequest
import json


class ConnectionInterface(Widget):
    def __init__(self, pos, size):
        super(ConnectionInterface, self).__init__()
        self.pos = pos
        self.size_hint = (None, None)
        self.size = size
        self.corner_radius = 20

        with self.canvas:
            Color(0, 0.8, 0)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius])


class Node(Widget):
    def __init__(self, name, **kwargs):
        super(Node, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.corner_radius = 20
        self.name = name

        self.interface_size = (20, self.size[1] - 2*self.corner_radius)

        with self.canvas:
            Color(0, 1, 0)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius])

        self.input_interface = ConnectionInterface(pos=[self.x - self.interface_size[0]/2, self.y + (self.size[1] - self.interface_size[1])/2], size=self.interface_size)
        self.add_widget(self.input_interface)
        self.output_interface = ConnectionInterface(pos=[self.x + self.width - self.interface_size[0]/2, self.y + (self.size[1] - self.interface_size[1])/2], size=self.interface_size)
        self.add_widget(self.output_interface)

        self.label = Label(text=self.name, pos=(self.x, self.y - 25), size_hint=(None, None), size=(100, 25))
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.init()

    def init(self):
        UrlRequest(f'http://localhost:5000/hello', on_success=self.init_response)

    def init_response(self, request, response):
        value = response.get('value', None)
        self.label.text = str(value)
