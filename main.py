from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from formEntry import FormEntry
from fileBrowser import FileBrowser


class MainMenu(Screen):
	"""
	Just a placeholder for the .kv which handles all the work
	"""
	pass


class Main(App):
	def build(self):
		screen_manager = ScreenManager(transition=FadeTransition())
		screen_manager.add_widget(MainMenu(name="MainMenu"))
		screen_manager.add_widget(FileBrowser(name="FileBrowser"))
		screen_manager.add_widget(FormEntry(name="FormEntry"))
		return screen_manager
		

if __name__ == "__main__":
	Main().run()
