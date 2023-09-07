from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import pygatt

class BluetoothApp(App):
    def __init__(self):
        super().__init__()
        self.bluetooth_adapter = pygatt.GATTToolBackend()

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.connect_button = Button(text='Connect to Bluetooth Device')
        self.connect_button.bind(on_press=self.scan_and_connect)
        self.layout.add_widget(self.connect_button)
        self.device_label = Label(text='')
        self.layout.add_widget(self.device_label)
        return self.layout

    def scan_and_connect(self, instance):
        try:
            self.bluetooth_adapter.start()
            devices = self.bluetooth_adapter.scan(timeout=10)
            esp32_device = None

            for device in devices:
                if "ESP32_LED_Control" in device["name"]:
                    esp32_device = device
                    break

            if esp32_device:
                self.device_label.text = f"Connecting to: {esp32_device['name']}"
                self.device = self.bluetooth_adapter.connect(esp32_device['address'])
                self.device_label.text = f"Connected to: {esp32_device['name']}"
                # Perform Bluetooth actions here, e.g., sending/receiving data
            else:
                self.device_label.text = "No ESP32 device found"
        except Exception as e:
            print(f"Failed to connect to the device: {e}")
        finally:
            self.bluetooth_adapter.stop()

if __name__ == '__main__':
    BluetoothApp().run()
