import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import pytesseract

def rotate(file):
    pdf_in = open(file, "rb")
    pdf = PdfReader(pdf_in)
    pages = pdf.pages
    pdf_writer = PdfWriter()
    for i in range(len(pages)):
        pages[i].rotate(90)
        pdf_writer.add_page(pages[i])
    with TemporaryDirectory() as tempdir:
        pdf_out = open(f"{tempdir}certificados.pdf", 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
    return f"{tempdir}certificados.pdf"

def build(file, folder):

    # Rotate the file.
    rotated_pdf = rotate(file)

    # Get pdf pages read as images.
    pdf_pages = convert_from_path(Path(rotated_pdf))

    #Check if folder certificados exists.
    MYDIR = (folder)
    CHECK_FOLDER = os.path.isdir(MYDIR)

    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(MYDIR)


    for page_enumeration, page in enumerate(pdf_pages, start=1):
        # Create a temporary directory to store generated image from page, as we do not need this file at the end of the execution.
        with TemporaryDirectory() as tempdir:
            filename = f"{tempdir}/temp_page.jpg"
            # Save page as image.
            page.save(filename, "JPEG")
            # Read image and execute ocr to get text.
            text = str(((pytesseract.image_to_string(Image.open(f"{tempdir}/temp_page.jpg")))))
            text = text.replace("-\n", "")
            # Get nit using regular expressions.
            match = re.search(r"Retuvo a.{1,}\n{1,2}Identificacion\D+([0-9]{1,})", text)
            # If a matching group exists, retrieve the corresponding information from the group. If no group exists, name the page with 'unknown' and the page number.
            if(match): nit = match.group(1)
            else: 
                nit = f"unknow_{page_enumeration}"
                print(text)
            # Save page using nit as name
            page.save(f"{folder}/{nit}.pdf", "PDF")