from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject

from notificationPopup import show_error_popup


def __set_need_appearances_writer(writer):
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
		show_error_popup("Error: __set_need_appearances_writer() catch : " + repr(e))     # pipe it to the main out.
		return writer


def __verify_pdf_acro_reader(pdf):
	if "/AcroForm" in pdf.trailer["/Root"]:
		pdf.trailer["/Root"]["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})


def __verify_pdf_acro_writer(pdf):
	if "/AcroForm" in pdf._root_object:
		pdf._root_object["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})


def write_pdf_from_template(pdf_template_path: str, pdf_write_path: str, variable_dictionary: dict):
	"""
	Writes a pdf with the fields supplied, as to match the template whose path is supplied.  Reads and writes all in one.
	:param pdf_template_path: template path (in our case, safety_checklist.pdf)
	:param pdf_write_path: output file path (user selected)
	:param variable_dictionary: form data which is used in a key-value set to the open PDF fields
	"""
	pdf_template = PdfFileReader(open(pdf_template_path, "rb"), strict=False)
	__verify_pdf_acro_reader(pdf_template)

	pdf_writer = PdfFileWriter()
	__set_need_appearances_writer(pdf_writer)
	__verify_pdf_acro_writer(pdf_writer)

	for page_num in range(pdf_template.numPages):
		pdf_writer.addPage(pdf_template.getPage(page_num))

	for page_num in range(pdf_template.numPages):
		pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(page_num), variable_dictionary)

	with open(pdf_write_path, 'wb') as f:
		pdf_writer.write(f)
