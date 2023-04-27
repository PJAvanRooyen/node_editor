import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, RoundedRectangle

import requests

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
    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)
        self.size_hint = (100, 100)
        self.size = (100, 100)
        self.corner_radius = 20

        self.interface_size = (20, self.size[1] - 2*self.corner_radius)

        with self.canvas:
            Color(0, 1, 0)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius])

        self.input_interface = ConnectionInterface(pos=[self.x - self.interface_size[0]/2, self.y + (self.size[1] - self.interface_size[1])/2], size=self.interface_size)
        self.add_widget(self.input_interface)
        self.output_interface = ConnectionInterface(pos=[self.x + self.width - self.interface_size[0]/2, self.y + (self.size[1] - self.interface_size[1])/2], size=self.interface_size)
        self.add_widget(self.output_interface)

        self.label = Label(text="Node", pos=(self.x, self.y - 25), size_hint=(None, None), size=(100, 25))
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            #if touch.is_double_tap:
            self.increment_value()

    def increment_value(self):
        # Get the value from the text input
        value = self.label.text

        if value == "Node":
            value = 1

        # Call the API using requests library
        response = requests.post('http://localhost:5000/increment', json={'value': value})

        # Get the result from the API response
        result = response.json()['result']

        # Update the label with the result
        self.label.text = '{}'.format(result)


class NodeEditor(FloatLayout):
    def __init__(self, **kwargs):
        super(NodeEditor, self).__init__(**kwargs)

        self.nodes = []
        self.line_start_node = None

    def on_touch_down(self, touch):
        super(NodeEditor, self).on_touch_down(touch)

        node_under_touch = False
        for node in self.nodes:
            if node.collide_point(*touch.pos) or node.input_interface.collide_point(*touch.pos) or node.output_interface.collide_point(*touch.pos):
                node_under_touch = True

            if node.output_interface.collide_point(*touch.pos):
                if 'line' not in touch.ud:
                    with self.canvas:
                        touch.ud['line'] = Line(points=[node.output_interface.center_x, node.output_interface.center_y, node.output_interface.center_x, node.output_interface.center_y], width=2)
                    self.line_start_node = node
                break

        if not node_under_touch:
            self.nodes.append(Node(pos=(touch.x, touch.y)))
            self.add_widget(self.nodes[-1])
        return True

    def on_touch_move(self, touch):
        super(NodeEditor, self).on_touch_move(touch)

        if 'line' in touch.ud:
            line_points = touch.ud['line'].points
            with self.canvas:
                touch.ud['line'].points = [line_points[0], line_points[1], touch.pos[0], touch.pos[1]]
        return True

    def on_touch_up(self, touch):
        super(NodeEditor, self).on_touch_up(touch)

        if 'line' in touch.ud:
            new_node_under_touch = False
            for node in self.nodes:
                if node.input_interface.collide_point(*touch.pos):
                    if self.line_start_node and self.line_start_node != node:
                        new_node_under_touch = True
                        line_points = touch.ud['line'].points
                        with self.canvas:
                            touch.ud['line'].points = [line_points[0], line_points[1], node.input_interface.center_x, node.input_interface.center_y]
                    break

            if not new_node_under_touch:
                self.canvas.remove(touch.ud['line'])

        self.line_start_node = None
        return True

    def on_double_tap(self):
        super(NodeEditor, self).on_double_tap()
        return True


class NodeEditorApp(App):
    def build(self):
        return NodeEditor()