import json
from fpdf import FPDF

def init_pdf():
    pdf = FPDF()
    pdf.add_page()
    return pdf

def generate_pdf(document , pdf,state):
    pdf.set_font("Arial", size=15)
    if state == "orders":
        pdf.set_text_color(0, 255, 0)
    elif state == "threat":
        pdf.set_text_color(255, 0, 0)
    else:
        pdf.set_text_color(0, 0, 0)
    with open("myfile.txt", 'w') as f:
        for key, value in document.items():
            f.write('%s:%s\n' % (key, value))
    pdf.set_font("Arial", size=15)
    f = open("myfile.txt", "r")
    for x in f:
        pdf.cell(200, 10, txt=x, ln=1, align='L')
    return pdf

def print_pdf(pdf):
    pdf.output("GFG.pdf")

document = {
    'ORDERS':'',
    1:'',
    'white_rice':'',
    'chicken':''
}
# pdf = init_pdf()
# pdf = generate_pdf(document=document,pdf=pdf)
# print_pdf(pdf)