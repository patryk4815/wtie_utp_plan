import io
from PyPDF2 import PdfFileReader, PdfFileWriter


def diff_pdf_pages(pdf1_path, pdf2_path):
    pdf2_fp = PdfFileReader(io.BytesIO(pdf2_path))
    pdf2_len = pdf2_fp.getNumPages()

    if not pdf1_path:
        return list(range(0, pdf2_len))

    pdf1_fp = PdfFileReader(io.BytesIO(pdf1_path))
    pdf1_len = pdf1_fp.getNumPages()

    list_differents = list()
    for i in range(pdf1_len):
        if i >= pdf2_len:
            list_differents.append(i)
            continue

        output1 = PdfFileWriter()
        output2 = PdfFileWriter()
        output1.addPage(pdf1_fp.getPage(i))
        output2.addPage(pdf2_fp.getPage(i))

        fp1 = io.BytesIO()
        fp2 = io.BytesIO()
        output1.write(fp1)
        output2.write(fp2)

        fp1.seek(0)
        fp2.seek(0)

        if fp1.read() != fp2.read():
            list_differents.append(i)
    return list_differents
