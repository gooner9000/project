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
            halign="right",
            multiline=False,
            background_color=[0.2,0.2,0.2,1],
            foreground_color=[1,1,1,1],
        )
        self.add_widget(self.result)

        buttons = [
            ["C","+/-","%","/"],
            ["7","8","9","*"],
            ["4","5","6","+"],
            ["1","2","3","-"],
            ["0","00",".","="]
        ]

        grid = GridLayout(cols=len(buttons[0]), spacing=2, padding=2)
        for row in buttons:
            for item in row:
                button = Button(
                    text=item,
                    font_size=45,
                    background_color=self.set_button_color(item),
                    color = 'white',
                    on_press=self.press
                )
                grid.add_widget(button)
        self.add_widget(grid)
    def set_button_color(self,label):
        if label in {"C","+/-","%"}:
            return [0.6,0.6,0.6,1]
        elif label in {"/","*","-","+","="}:
            return [1.5,0.6,0.6,1]
        return[0.3,0.3,0.3,1]

    def press(self, instance):
        text = instance.text

        if text == "C":
            self.result.text = ""
        elif self.result.text != "ERROR":
            if text == "+/-":
                self.toggle_neg()
            elif text == "%":
                self.convert_percent()
            elif text == "=":
                self.calculate()
            else:
                self.result.text += text

    def calculate(self):
        try:
            self.result.text = str(eval(self.result.text))
        except Exception:
            self.result.text = "ERROR"
        return self.result.text

    def toggle_neg(self):
        if self.result.text:
            self.result.text = self.result.text[1:] if self.result.text[0] == "-" else "-" + self.result.text

    def convert_percent(self):
        try:
            self.result.text = str(float(self.result.text)/100)
        except ValueError:
            self.result.text = "ERROR"
class CalculatorApp(App):
    def build(self):
        return Calculator()

if __name__ == "__main__":
    CalculatorApp().run()

