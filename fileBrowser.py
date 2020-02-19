from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


class FileBrowser(Screen):
	"""
	A file browser which needs to operate either in the open or write mode, doing recursive directory walk.
	"""

	# TODO: all of this
	write_mode = False


# TODO: why is this having to be loaded manually, but main.py works fine with main.kv?
Builder.load_file("fileBrowser.kv")
