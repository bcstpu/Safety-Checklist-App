from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

from notificationPopup import show_error_popup, show_success_popup


class FileBrowser(Screen):
	"""
	A file browser which needs to operate either in the open or save mode, doing recursive directory walk.
	# TODO: there's a lot of instance/static that should be swapped around, but Kivy likes to throw a fit when it's expecting one or the other.
	"""

	__OPERATION_BUTTON_SAVE_TEXT = "Save"
	__OPERATION_BUTTON_LOAD_TEXT = "Load"
	__SAVE_SUCCESS_TEXT = "We haven't saved but we would've if this was coded in!"
	__SAVE_FAILURE_TEXT = "Failed to save."
	__SAVE_NO_NAME_TEXT = "No name supplied for file."
	__SAVE_INVALID_DIR_TEXT = "Please select a valid directory to save in."
	__LOAD_INVALID_DIR_TEXT = "Please select a valid file to load."
	__LOAD_FAIL_TEXT = "Could not load the file: "

	_save_mode = False
	_file_path = ""
	_file_name = ""
	_operation_button_label_text = "OK"  # TODO: dynamically set this off save/load mode

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	@staticmethod
	def set_file_name(name: str):
		if type(name) is str:
			FileBrowser._file_name = name
		else:
			FileBrowser._file_name = str(name)

	@staticmethod
	def _operation_button_text() -> str:
		if FileBrowser._save_mode:
			return FileBrowser.__OPERATION_BUTTON_SAVE_TEXT
		return FileBrowser.__OPERATION_BUTTON_LOAD_TEXT

	# unfortunately, these have to be instance-based methods, thanks to kivy widget binding
	# TODO: figure out how to make these static?
	def _set_file_path(self, s: str):
		FileBrowser._file_path = str(s)  # for some reason it sometimes sends it as a list?

	def _set_file_name(self, s: str):
		FileBrowser._file_name = s

	def _operation(self):
		"""
		Performs the operation of the operation (save/load) button press, and all control flow from.
		It will also switch the root back to the main window on operation success, along with popups and such through subroutines.
		"""
		if (FileBrowser._file_path is None) or (FileBrowser._file_path == ""):
			FileBrowser._operation_error()
			return False

		if FileBrowser._save_mode:
			operation_succeeded = FileBrowser._save()
		else:
			operation_succeeded = FileBrowser._load()

		if operation_succeeded:
			self.manager.current = 'MainMenu'

	@staticmethod
	def _operation_error():
		show_error_popup(FileBrowser.__SAVE_INVALID_DIR_TEXT if FileBrowser._save_mode else FileBrowser.__LOAD_INVALID_DIR_TEXT)

	@staticmethod
	def _load() -> bool:
		if FileBrowser._file_path is not None:
			try:
				os.startfile(FileBrowser._file_path)
				return True
			except:
				show_error_popup(FileBrowser.__LOAD_FAIL_TEXT + FileBrowser._file_path)
				return False

	@staticmethod
	def _save() -> bool:
		if (FileBrowser._file_path is None) or (FileBrowser._file_path == ""):
			show_error_popup(FileBrowser.__SAVE_INVALID_DIR_TEXT)
			return False

		if FileBrowser._file_name == "":
			show_error_popup(FileBrowser.__SAVE_NO_NAME_TEXT)
			return False

		# TODO: actually save
		saved = True
		if saved:
			show_success_popup("We haven't implemented saving " + FileBrowser._file_path + "!")
			return True
		else:
			show_error_popup(FileBrowser.__SAVE_FAILURE_TEXT)
			return False

	@staticmethod
	def cleanup():
		FileBrowser._file_path = ""
		FileBrowser._file_name = ""
		FileBrowser._save_mode = False





Builder.load_file("fileBrowser.kv")
