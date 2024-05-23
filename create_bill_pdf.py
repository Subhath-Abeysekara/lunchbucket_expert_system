import time

from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from sendMail import send_mail_bill

# Sample data
# data = {
#     '1': {'customer_code': 4, 'order_code': 0,'price': 0},
#     '20': {'customer_code': 4, 'order_code': 0,'price': 0},
#     '2': {'customer_code': 4, 'order_code': 0,'price': 0},
#     '3': {'customer_code': 4, 'order_code': 0,'price': 0},
#     '4': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '5': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '6': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '7': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '8': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '10': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '11': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '12': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '13': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '14': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '15': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '16': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '17': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '18': {'customer_code': 4, 'order_code': 0, 'price': 0},
#     '19': {'customer_code': 4, 'order_code': 0, 'price': 0},
# }

def create_bill_pdf(data):
    # Create a canvas object
    filename = "bill_document.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # # Title
    # c.setFont("Helvetica-Bold", 16)
    # c.drawString(100, height - 50, f"LIMIT PREDICTION - {meal}")
    y = height - 50
    c.setFont("Helvetica", 12)

    # Iterate through the dictionary and add text to the PDF
    box_width = int((width - 100 )/ 3)  # Width of the box
    box_height = int((height - 100)/5)  # Height of the box
    padding = 10
    mini_box_width = box_width  # Width of the box
    mini_box_height = box_height - 10  # Height of the box
    mini_padding = 5

    image_path = "LB_LOGO.png"
    image_width = 20  # Set the width of the image
    image_height = 20
    x = 20
    font1 = 12
    font2 = 10
    # Padding inside the box
    for key, value in data.items():
        if y < 80:  # Check if the y-coordinate is too low, add a new page if needed
            c.showPage()
            y = height - 50
            x = 20
        y_old = y
        c.setStrokeColorRGB(0, 0, 0)  # Black color for the border
        c.setLineWidth(2)  # Border width
        c.rect(x - padding, y - box_height, box_width + padding * 2, box_height)
        y-=5
        x+=5
        c.setLineWidth(1)  # Border width
        c.rect(x - padding, y - mini_box_height, mini_box_width + mini_padding * 2, mini_box_height)
        y-=20
        x+=10
        c.drawImage(image_path, x - padding, y - 10  , image_width, image_height)
        c.setFont("Helvetica-Bold", font2)
        text = f"0{key.capitalize()}" if len(str(key)) == 1 else f"{key.capitalize()}"
        c.drawString(x+box_width-30, y, text)
        c.setFont("Helvetica-Bold", font1)
        text = f"Lunch Bucket"
        c.drawString(x + image_width + 10, y - 5, text)
        y -= 28  # Move down for the next line
        c.setFont("Helvetica-Bold", font2)
        text = f"Customer Code"
        c.drawString(x, y, text)
        y -= 10
        x += 20
        c.setFont("Helvetica", font2)
        text = f"{value['customer_code']}"
        c.drawString(x, y, text)
        y -= 3
        x -= 20
        text = f"__ __ __ __ __ __ __ __ __"
        c.drawString(x, y, text)
        y -= 20
        c.setFont("Helvetica-Bold", font2)
        text = f"Order Code"
        c.drawString(x, y, text)
        y -= 10
        x += 20
        c.setFont("Helvetica", font2)
        text = f"{value['order_code']}"
        c.drawString(x, y, text)
        y -= 3
        x -= 20
        text = f"__ __ __ __ __ __ __ __ __"
        c.drawString(x, y, text)
        y -= 20
        c.setFont("Helvetica-Bold", font2)
        text = f"Price"
        c.drawString(x, y, text)
        y -= 10
        x += 20
        c.setFont("Helvetica", font2)
        text = f"{value['price']}"
        c.drawString(x, y, text)
        y -= 3
        x -= 20
        text = f"__ __ __ __ __ __ __ __ __"
        c.drawString(x, y, text)

        if x > 2*width / 3:
            x = 20
            y -= 15
        elif x> width / 3:
            x = 2*(box_width + 30)
            y = y_old
        else:
            x = box_width + 40
            y = y_old
    c.save()
    time.sleep(2)
    send_mail_bill()

# create_bill_pdf(data)
#
# print("PDF created successfully!")