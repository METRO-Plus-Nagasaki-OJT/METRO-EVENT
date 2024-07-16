import qrcode
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
import os

def create_qr(id):
    logo_path = "../common/present_hub_logo.png"
    logo = Image.open(logo_path)
    basewidth = 100
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    QRcode = qrcode.QRCode(version=6,
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data(id)
    QRcode.make()
    QRimg = QRcode.make_image(
    fill_color=(63,131,248), back_color="white").convert('RGB')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos, mask=logo)
    
    QRimg.save('../common/QR.png')

def send_qr(email):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "presenthub.co.24@gmail.com"
    password = "legend@rypurojecto322"
    subject = "Test Email from Present Hub"
    body = "This is a test email sent from a Present Hub."
    image_path = "../common/QR.png"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject 
    message.attach(MIMEText(body, "plain"))
    with open(image_path, "rb") as image_file:
        mime_image = MIMEImage(image_file.read())
        mime_image.add_header('Content-Disposition', f'attachment; filename="{image_path.split("/")[-1]}"')
        message.attach(mime_image)
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server.quit()
        if os.path.exists(image_path):
            os.remove(image_path)