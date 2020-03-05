from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

from notificationPopup import show_error_popup, show_success_popup
from pdfWriter import write_pdf_from_template
from shutil import copy


class FileBrowser(Screen):
	"""
	A file browser which needs to operate either in the open or save mode, doing recursive directory walk.
	# TODO: there's a lot of instance/static that should be swapped around, but Kivy likes to throw a fit when it's expecting one or the other.
	"""

	__SAVE_SUCCESS_TEXT = "File saved."
	__SAVE_FAILURE_TEXT = "Failed to save."
	__SAVE_NO_NAME_TEXT = "No name supplied for file."
	__SAVE_INVALID_DIR_TEXT = "Please select a valid directory to save in."
	__LOAD_INVALID_DIR_TEXT = "Please select a valid file to load."
	__LOAD_FAIL_TEXT = "Could not load the file: "
	__TEMPLATE_PATH = "safety_checklist.pdf"

	__DEBUG_NAME = "debug output"

	_save_mode = False
	_file_path = ""
	_file_name = ""
	_operation_button_label_text = "OK"
	_write_fields = {}

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	@staticmethod
	def set_write_data(fields: dict):
		"""
		Sets the write data of fields and, by extension of these fields, the file name
		:param fields: the fields object from formentry sent in to be held in the fileBrowser data buffer
		:return: none
		"""
		# paths don't like slashes.
		date_field = fields["day_and_date"]
		date_str_a = date_field.replace("/", "-")
		date_str_b = date_str_a.replace("\\", "-")

		FileBrowser._file_name = "" + fields["first_name"] + "-" + fields["last_name"] + "-" + date_str_b + ".pdf"
		if FileBrowser._file_name == "--.pdf":
			FileBrowser._file_name = FileBrowser.__DEBUG_NAME + ".pdf"

		FileBrowser._write_fields = fields

	# unfortunately, these have to be instance-based methods, thanks to kivy widget binding
	# TODO: rewrite some of the binding code to properly reference static, then refactor
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

		# first copies over the template; Steven's implementation really fucked us over here
		file_total_path = os.path.join(FileBrowser._file_path, FileBrowser._file_name)
		"""
		try:
			copy(FileBrowser.__TEMPLATE_PATH, file_total_path)
		except Exception as e:
			show_error_popup("Couldn't create a PDF template to write on.\nTarget path: " + file_total_path + "\nError: " + repr(e))
			return False
		"""
		# then writes to it
		write_pdf_from_template(FileBrowser.__TEMPLATE_PATH, file_total_path, FileBrowser._write_fields)
		show_success_popup("Saved to " + file_total_path + ".")
		FileBrowser.__cleanup()
		return True

	@staticmethod
	def __cleanup():
		FileBrowser._file_path = ""
		FileBrowser._file_name = ""
		FileBrowser._save_mode = False


Builder.load_file("fileBrowser.kv")
