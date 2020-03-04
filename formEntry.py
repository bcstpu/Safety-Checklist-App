from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from licensing import is_valid_license
from notificationPopup import show_error_popup


class FormEntry(Screen):
	"""
	This is the main form entry class.
	On init, declare a formatted dict that can be hooked up to the PDF function.
	Initializing values to None and then overwriting when the form is completed will handle absent field checking.
	"""

	__MAXIMUM_LINES_OF_MISSING_FIELDS = 5  # what will display on a popup usually
	__OVERRIDE_ERRORS = True
	__FIELDS_MISSING_POPUP_TEXT = "Missing Fields:\n"

	@staticmethod
	def __missing_fields(form: dict) -> list:
		"""
		Returns a list of fields which are still marked as None; useful for debugging or error popups.
		:return: fields which are still missing values a list of their keys
		"""
		s = []
		for key in form.keys():
			if (form[key] is None) or (form[key] == ""):
				s.append(key)
		return s

	@staticmethod
	def __check_business_logic(form: dict) -> str:
		"""
		Checks the business logic layer and returns an error message string.
		If no errors are found it will return just an empty string.
		:param form:
		:return: string for error message
		"""
		return ""

	@staticmethod
	def __engineer_name_and_license(form: dict) -> tuple:
		engineer_name = (form["first_name"] if form["first_name"] else "") + " " + (form["last_name"] if form["last_name"] else "")
		engineer_license_number = form["lic_num"] if form["lic_num"] else ""
		return engineer_name, engineer_license_number

	@staticmethod
	def __missing_fields_string(missing_fields: list, max_lines: int) -> str:
		s = ""
		added = 0
		for field in missing_fields:
			if added < max_lines:
				s += field
				added += 1
				if added < max_lines:
					s += "\n"
		return s

	def pressed_save(self):
		"""
		Subroutine that runs when save is pressed.
		Checks that the engineer is licensed, and if not returns a popup.
		If engineer is licensed, transitions to file browser to save
		"""

		form = self.build_key_value_pairs()

		# check for missing fields
		missing_fields = FormEntry.__missing_fields(form)
		if missing_fields:
			show_error_popup(FormEntry.__FIELDS_MISSING_POPUP_TEXT + FormEntry.__missing_fields_string(missing_fields, FormEntry.__MAXIMUM_LINES_OF_MISSING_FIELDS))
			if not FormEntry.__OVERRIDE_ERRORS:
				return

		# check the business logic
		business_logic_errors = FormEntry.__check_business_logic(form)
		if business_logic_errors != "":
			show_error_popup(business_logic_errors)
			if not FormEntry.__OVERRIDE_ERRORS:
				return

		# check the engineer name and licensing
		engineer_name_and_license = FormEntry.__engineer_name_and_license(form)
		if not is_valid_license(engineer_name_and_license[0], engineer_name_and_license[1]):
			show_error_popup("Could not verify proper licensing.\nName: \"" + engineer_name_and_license[0] + "\"\nID: " + engineer_name_and_license[1] + "")
			if not FormEntry.__OVERRIDE_ERRORS:
				return

		# transfer to file browser to save
		show_error_popup("Passing to file browse,r but it's uh, yeah, not done yet.")

	def build_key_value_pairs(self):
		"""
		Some seriously weird stuff.  Introspects the self.ids, determines by what fields they have if it's text or checkbox.
		From there it adds to a dict of values.  Kivy text objects have text as their field name, kivy checkboxes have active.
		:return: key-value dictionary
		"""
		values = {}
		for id_field in self.ids:
			if hasattr(getattr(self, id_field), "text"):
				values[id_field] = getattr(self, id_field).text
			elif hasattr(getattr(self, id_field), "active"):
				values[id_field] = getattr(self, id_field).active
			else:
				print("Error on " + id_field)
		return values


# Builder.load_file("wzsafetychecklist.kv")
Builder.load_file("formEntry.kv")   # TODO: get the valid one from Reynaldo.
