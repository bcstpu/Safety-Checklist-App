__LICENSING_PATH = "licenses.txt"


def __format_to_tolerance(s: str) -> str:
	return s.upper().lstrip().rstrip()


def __parse_license_line(line: str) -> tuple:
	split = line.split(":")
	name = __format_to_tolerance(split[0])
	key = __format_to_tolerance(split[1])
	return name, key


def _load_keys(file_path: str) -> dict:
	"""
	Loads from a text file on disk the key-value pair of engineer names and their authentication keys.
	These keys and names are also formatted while loaded to provide case-inensitivity and whitespace-insensitivity.
	:param file_path: the path of the text file used for lookup
	:return: the dict which contains the name-authcode pairs
	"""
	key_values = {}
	with open(file_path, 'r') as file:
		for line in file:
			line_values = __parse_license_line(line)
			key_values[line_values[0]] = line_values[1]
	return key_values


def _matches_keys(name: str, key: str, licenses: dict) -> bool:
	"""
	Returns if a name and key, matches the licenses dict supplied
	:param name: Name of the engineer to match
	:param key: Key or authentication code of the engineer
	:param licenses: the licenses dictionary of keys and names
	:return: if the license lookup is valid
	"""
	formatted_name = __format_to_tolerance(name)
	formatted_key = __format_to_tolerance(key)
	if licenses.keys().__contains__(formatted_name):
		if licenses[formatted_name] == formatted_key:
			return True
	return False


def is_valid_license(name: str, key: str) -> bool:
	return _matches_keys(name, key, _load_keys(__LICENSING_PATH))
