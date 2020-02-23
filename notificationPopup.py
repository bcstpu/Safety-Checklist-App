from kivy.uix.popup import Popup
from kivy.uix.button import Button


_ERROR_POPUP_SIZE_HINT = (0.75, 0.5)
_ERROR_DEFAULT_WINDOW_TEXT = "Warning"
_SUCCESS_DEFAULT_WINDOW_TEXT = "Success"


def __raw_popup(window_title: str, button_message: str):
	content = Button(text=button_message)
	popup = Popup(title=window_title, content=content, size_hint=_ERROR_POPUP_SIZE_HINT)
	content.bind(on_press=popup.dismiss)
	popup.open()


def show_error_popup(button_message: str):
	"""
	Creates a simple button popup with the message specified and a "warning" label, for things like user error.
	:param button_message: The text to show on the button that covers the popup
	"""
	__raw_popup(_ERROR_DEFAULT_WINDOW_TEXT, button_message)


def show_success_popup(button_message: str):
	"""
	Creates a simple button popup with the message specified and a "show_success" label, for things like saving a file.
	:param button_message: The text to show on the button that covers the popup
	"""
	__raw_popup(_SUCCESS_DEFAULT_WINDOW_TEXT, button_message)
