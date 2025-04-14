
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from src.core.ecu_manager import ECUManager
from src.core.backup_manager import BackupManager

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.ecu_manager = ECUManager()
        self.backup_manager = BackupManager()
        self.current_file = None

        # File chooser
        self.file_chooser = FileChooserIconView()
        self.add_widget(self.file_chooser)

        # Buttons
        button_layout = BoxLayout(size_hint_y=0.1)

        load_button = Button(text="Load File")
        load_button.bind(on_press=self.load_file)
        button_layout.add_widget(load_button)

        save_button = Button(text="Save File")
        save_button.bind(on_press=self.save_file)
        button_layout.add_widget(save_button)

        backup_button = Button(text="Create Backup")
        backup_button.bind(on_press=self.create_backup)
        button_layout.add_widget(backup_button)

        self.add_widget(button_layout)

        # Status label
        self.status_label = Label(text="Status: Ready", size_hint_y=0.1)
        self.add_widget(self.status_label)

    def load_file(self, instance):
        selected = self.file_chooser.selection
        if selected:
            try:
                self.current_file = selected[0]
                success, message = self.ecu_manager.load_file(self.current_file)
                if success:
                    self.status_label.text = f"Loaded: {self.current_file}"
                else:
                    self.show_popup("Error", message)
            except Exception as e:
                self.show_popup("Error", str(e))

    def save_file(self, instance):
        if not self.current_file:
            self.show_popup("Warning", "No file loaded")
            return

        try:
            success, message = self.ecu_manager.save_file(self.current_file)
            if success:
                self.status_label.text = "File saved successfully"
            else:
                self.show_popup("Error", message)
        except Exception as e:
            self.show_popup("Error", str(e))

    def create_backup(self, instance):
        if not self.current_file:
            self.show_popup("Warning", "No file loaded")
            return

        try:
            self.backup_manager.create_backup(self.ecu_manager.get_data())
            self.status_label.text = "Backup created successfully"
        except Exception as e:
            self.show_popup("Error", str(e))

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class ECUToolApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    ECUToolApp().run()
