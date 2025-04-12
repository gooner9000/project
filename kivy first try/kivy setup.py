from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

Window.size = (300,500)

class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical',**kwargs)

        # Build out the app
        self.result = TextInput(
            font_size=45,
            size_hint_y=0.2,
            readonly=True,
            halign="right"
            multiline=False,
        )



class CalculatorApp(App):
    def build(self):
        return Calculator()

if __name__ == "__main__":
    CalculatorApp().run()

