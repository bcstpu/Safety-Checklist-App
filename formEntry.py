from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from licensing import is_valid_license


class FormEntry(Screen):
	"""
	This is the main form entry class.
	On init, declare a formatted dict that can be hooked up to the PDF function.
	Initializing values to None and then overwriting when the form is completed will handle absent field checking.
	"""

	form_data = {}

	@staticmethod
	def reset_form_data():
		"""
		TODO: fill in with the proper fields as per VDOT form
		"""
		FormEntry.form_data = {
			"Working fields": None,
			"Work done yet": None,
			"Is a good example?": False
		}

	@staticmethod
	def _is_valid_form() -> bool:
		"""
		Subroutine to verify form_data matches expected values; checks missing fields and for valid license.
		TODO: refactor to functional form?
		"""
		for field in FormEntry.form_data:
			if(field is None) or (field == ""):
				return False
		return is_valid_license(FormEntry.form_data["Name"], FormEntry.form_data["ID"])

	@staticmethod
	def _missing_fields() -> list:
		"""
		Returns a list of fields which are still marked as None; useful for debugging or error popups.
		:return: fields which are still missing values a list of their keys
		"""
		s = []
		for key in FormEntry.form_data.keys():
			if FormEntry.form_data[key] is None:
				s.append(key)
		return s

	def __init__(self, **kwargs):
		"""
		Constructor for the formEntry panel and data; layout is defined in the .kv file to separate presentation and data model.
		"""
		super(FormEntry, self).__init__(**kwargs)
		FormEntry.reset_form_data()


# TODO: why is this having to be loaded manually, but main.py works fine with main.kv?
Builder.load_file("formEntry.kv")
