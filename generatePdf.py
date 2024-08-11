import json
from fpdf import FPDF

def init_pdf():
    pdf = FPDF()
    pdf.add_page()
    return pdf

def generate_pdf(document , pdf,state , large_state = False):
    pdf.set_font("Arial", size=15)
    if state == "orders":
        pdf.set_text_color(0, 255, 0)
    elif state == "threat":
        pdf.set_text_color(255, 0, 0)
    elif state == "printed":
        pdf.set_text_color(139, 69, 19)
        if large_state:
            pdf.set_text_color(92,64,51)
    elif state == 'priority':
        pdf.set_text_color(0,180,0)
        if large_state:
            pdf.set_text_color(0,100,0)
    elif state == 'normal':
        pdf.set_text_color(0, 0, 230)
        if large_state:
            pdf.set_text_color(0,0,100)
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
class PDFWithTable(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Order Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def add_table(self, data, header=True):
        if header:
            # Add table header
            self.set_font('Arial', 'B', 12)
            i=0
            for col in data[0]:
                if i == 0:
                    self.cell(90, 10, col, 1)
                    i+=1
                else:
                    self.cell(20, 10, col, 1)
            self.ln()

        # Add table rows
        self.set_font('Arial', '', 12)
        for row in data[1:]:
            i=0
            for col in row:
                self.set_text_color(0, 0, 0)
                if i==0:
                    self.cell(90, 10, str(col), 1)
                    i+=1
                else:
                    if i % 2 == 0:
                        self.set_text_color(255, 0, 0)
                    self.cell(10, 10, str(col), 1)
                    i+=1
            self.ln()

document = {
    'ORDERS':'',
    1:'',
    'white_rice':'',
    'chicken':''
}
# pdf = init_pdf()
# pdf = generate_pdf(document=document,pdf=pdf)
# print_pdf(pdf)