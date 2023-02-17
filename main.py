from pynput import mouse, keyboard
import datetime 
import json
import os

class MyException(Exception): pass


class Recorder():
    def __init__(self, location: str):
        self.mouse_data = {}
        self.keyboard_data = {}
        self.location = location

        if not os.path.exists(self.location):
            os.mkdir(self.location)

    def on_press(self, key):
        self.keyboard_data[datetime.datetime.now().isoformat()] = {"press": {"key": str(key)}}

    def on_release(self, key: keyboard.Key):
        self.keyboard_data[datetime.datetime.now().isoformat()] =  {"press": {'release': str(key)}}
        
        if key == keyboard.Key.esc:
            # Stop listener
            self.save_keyboard_data()
            self.save_mouse_data()
            raise MyException('Stop')

    def save_keyboard_data(self):
        with open(f'{self.location}/keyboard_data.json', 'w') as f:
            json.dump(self.keyboard_data, f)

    def save_mouse_data(self):
        with open(f'{self.location}/mouse_data.json', 'w') as f:
            json.dump(self.mouse_data, f)

    def on_move(self, x, y):
        self.mouse_data[datetime.datetime.now().isoformat()] = {"move": {"coords": [x, y]}}
        print(datetime.datetime.now(), x, y)

    def on_click(self, x, y, button, pressed):
        self.mouse_data[datetime.datetime.now().isoformat()] = {"click": {"coords": [x, y], "button": str(button), "pressed": pressed}}
        print(datetime.datetime.now(), x, y, button, pressed)

    def on_mb_release(self, x, y, button, pressed):
        self.mouse_data[datetime.datetime.now().isoformat()] = {"release": {"coords": [x, y], "button": str(button), "pressed": pressed}}
        print(datetime.datetime.now(), x, y, button, pressed)

    def on_scroll(self, x, y, dx, dy):
        self.mouse_data[datetime.datetime.now().isoformat()] = {"scroll": {"coords": [x, y], "dx": dx, "dy": dy}}

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as K_listener: # type: ignore
            with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll, on_release=self.on_mb_release) as M_listener:
                try:
                    K_listener.join()
                    M_listener.join()
                except MyException:
                    print('Stop')

class Player():
    
    def __init__(self, location: str):
        self.mouse_data = json.loads(open(f'{location}/mouse_data.json').read())
        self.keyboard_data = json.loads(open(f'{location}/keyboard_data.json').read())
        self.data_list = list(self.mouse_data.items()) + list(self.keyboard_data.items())
        self.data_list = sorted(self.data_list, key=lambda x: x[0])
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
    
    def play(self):
        for i in range(len(self.data_list)):
            og_time = datetime.datetime.now()
            current = self.data_list[i]

            try:
                next = self.data_list[i+1]
            except IndexError:
                break
            
            # calculate the time difference between the current and next data point
            current_time = datetime.datetime.fromisoformat(current[0])
            next_time = datetime.datetime.fromisoformat(next[0])
            data_time_diff = next_time - current_time

            current_time_diff = datetime.datetime.now() - og_time

            while current_time_diff < data_time_diff:
                current_time_diff = datetime.datetime.now() - og_time

                if current_time_diff >= data_time_diff:
                    print(next[1])
                    if next[1].get('move'):
                        self.mouse.position = next[1].get('move').get('coords')
                    elif next[1].get('click'):
                        if (next[1].get('click').get('button') == 'Button.left'):
                            self.mouse.click(button = mouse.Button.left)
                        elif (next[1].get('click').get('button') == 'Button.right'):
                            self.mouse.click(button = mouse.Button.right)

                    elif next[1].get('press').get('key'):
                        if (next[1].get('press').get('key').split('.')[0] == 'Key'):
                            self.keyboard.press(getattr(keyboard.Key, next[1].get('press').get('key').split('.')[1]))
                        else:
                            self.keyboard.press(next[1].get('press').get('key').strip("'"))
                        
                    elif next[1].get('press').get('release'):
                        # if (next[1].get('press').get('release').split('.')[0] == 'Key'):
                        #     print(next[1].get('press').get('release').split('.')[1], getattr(keyboard.Key, next[1].get('press').get('release').split('.')[1]))
                        #     keyboard.Controller().release(getattr(keyboard.Key, next[1].get('press').get('release').split('.')[1]))
                        # keyboard.Controller().release(next[1].get('press').get('release'))
                        pass
                    break

