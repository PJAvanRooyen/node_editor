from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line

from src.node_editor_view.node import Node


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
            self.nodes.append(Node(name='increment', pos=(touch.x, touch.y)))
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