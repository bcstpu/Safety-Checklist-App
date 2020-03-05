from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from notificationPopup import show_error_popup


def set_need_appearances_writer(writer):
	"""Fixes glitches in backend of pdf writer, see: https://github.com/mstamy2/PyPDF2/issues/355#issuecomment-360575792"""
	try:
		catalog = writer._root_object
		# get the AcroForm tree and add "/NeedAppearances attribute
		if "/AcroForm" not in catalog:
			writer._root_object.update({
				NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

		need_appearances = NameObject("/NeedAppearances")
		writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
		return writer

	except Exception as e:
		show_error_popup("Error: set_need_appearances_writer() catch : " + repr(e))     # pipe it to the main out.
		return writer


def __verify_pdf_acro_reader(pdf):
	if "/AcroForm" in pdf.trailer["/Root"]:
		pdf.trailer["/Root"]["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})


def __verify_pdf_acro_writer(pdf):
	if "/AcroForm" in pdf._root_object:
		pdf._root_object["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})


def write_pdf_from_template(pdf_template_path: str, pdf_write_path: str, variable_dictionary: dict) -> bool:
	# dump to command line the entire var dict.
	print("WRITING THESE FIELDS:")
	for key in variable_dictionary.keys():
		print("Field Name: " + key + " Value: " + variable_dictionary[key])

	pdf_template = PdfFileReader(open(pdf_template_path, "rb"), strict=False)
	__verify_pdf_acro_reader(pdf_template)

	pdf_writer = PdfFileWriter()
	set_need_appearances_writer(pdf_writer)
	__verify_pdf_acro_writer(pdf_writer)

	# page add --I guess it's a page at a time?  No idea why steven's original has this, but w/e
	for page_num in range(pdf_template.numPages):
		pdf_writer.addPage(pdf_template.getPage(page_num))
		pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(page_num), variable_dictionary)

	# wanna see me do it again?  I don't think it's writing right until finished compilation but I don't know...
	for page_num in range(pdf_template.numPages):
		pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(page_num), variable_dictionary)

	# save
	with open(pdf_write_path, 'wb') as f:
		pdf_writer.write(f)
	return True


def createPDF(pdf_path, variableDictionary):
	pdf_writer = PdfFileWriter()
	set_need_appearances_writer(pdf_writer)
	pdf_reader = PdfFileReader(pdf_path)
	page_1 = pdf_reader.getPage(0)
	pdf_writer.addPage(page_1)
	pdf_writer.updatePageFormFieldValues(page_1, variableDictionary)
	with open('completed_checklist.pdf', 'wb') as fh:
		pdf_writer.write(fh)

"""
if __name__ == '__main__':
	path = 'safety_checklist.pdf'
"""
