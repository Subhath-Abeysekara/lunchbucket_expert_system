import time

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from sendMail import send_ml_limits

# Sample data
# data = {
#     'white rice': {'limit': 4, 'pre_request': 0},
#     'red rice': {'limit': 3, 'pre_request': 0},
#     'white rice1': {'limit': 4, 'pre_request': 0},
#     'red rice1': {'limit': 3, 'pre_request': 0},
#     'white rice2': {'limit': 4, 'pre_request': 0},
#     'red rice2': {'limit': 3, 'pre_request': 0},
#     'white rice3': {'limit': 4, 'pre_request': 0},
#     'red rice3': {'limit': 3, 'pre_request': 0},
#     'white rice4': {'limit': 4, 'pre_request': 0},
#     'red rice4': {'limit': 3, 'pre_request': 0},
#     'white rice5': {'limit': 4, 'pre_request': 0},
#     'red rice5': {'limit': 3, 'pre_request': 0},
#     'white rice6': {'limit': 4, 'pre_request': 0},
#     'red rice6': {'limit': 3, 'pre_request': 0},
#     'white rice7': {'limit': 4, 'pre_request': 0},
#     'red rice7': {'limit': 3, 'pre_request': 0},
#     # 'white rice2': {'limit': 4, 'pre_request': 0},
#     # 'red rice2': {'limit': 3, 'pre_request': 0},
#     # 'white rice3': {'limit': 4, 'pre_request': 0},
#     # 'red rice3': {'limit': 3, 'pre_request': 0},
#     # 'white rice4': {'limit': 4, 'pre_request': 0},
#     # 'red rice4': {'limit': 3, 'pre_request': 0},
#     # 'white rice5': {'limit': 4, 'pre_request': 0},
#     # 'red rice5': {'limit': 3, 'pre_request': 0},
# }

def create_limit_pdf(data , meal):
    filename = "ml_limit_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, f"LIMIT PREDICTION - {meal}")
    y = height - 100
    c.setFont("Helvetica", 12)
    i = 1
    for key, value in data.items():
        if y < 80:
            c.showPage()
            y = height -100
        c.setFont("Helvetica-Bold", 12)
        text = f"{i} - {key.capitalize()}"
        c.drawString(100, y, text)
        y -= 20
        c.setFont("Helvetica", 12)
        text = f"Pre-request: {value['pre_request']}"
        c.drawString(120, y, text)
        y -= 20
        text = f"Limit: {value['limit']}"
        c.drawString(120, y, text)
        y -= 25
        i+=1
    c.save()
    time.sleep(3)
    send_ml_limits()

# create_limit_pdf(data , 'Dinner')
#
# print("PDF created successfully!")
