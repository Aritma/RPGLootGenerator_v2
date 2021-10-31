from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import StringProperty


class JsonViewer(Label):
    text_value = StringProperty()


class AppGUI(App):
    with open('gui/test.json', 'r') as file:
        JsonViewer.text_value = file.read()


if __name__ == '__main__':
    AppGUI().run()
