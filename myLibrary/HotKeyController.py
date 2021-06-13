import keyboard


class StartStop:
    def __init__(self):
        self.pause = None
        self.stop = None
        self.web_site = None

        keyboard.add_hotkey('Ctrl + P', self.pause)
        print('Ctrl + P')

        keyboard.add_hotkey('Ctrl + S', self.stop)
        print('Ctrl + S')
