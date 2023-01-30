import cgi
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from fpdf import FPDF

form = cgi.FieldStorage()
to_email = form.getvalue("email")
file_item = form["file"]

if file_item.filename:
    # strip leading path from file name to avoid directory traversal attacks
    fn = os.path.basename(file_item.filename)
    open(fn, 'wb').write(file_item.file.read())

    # function to convert file to pdf
    def convert_to_pdf(file_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        with open(file_path, "r") as f:
            for line in f:
                pdf.cell(200, 10, txt=line, ln=1, align="C")
        pdf_file_path = file_path.split(".")[0] + ".pdf"
        pdf.output(pdf_file_path)
        return pdf_file_path

    # function to send email with pdf attachment
    def send_email(to, pdf_file_path):
        from_email = "mailsrisaradaengineering@gmail.com"
        from_password = "Neeraj123%"
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to
        msg['Subject'] = "Converted PDF File"
        body = "Please find attached the converted pdf file."
        msg.attach(MIMEText(body, 'plain'))
        pdf_file = open(pdf_file_path, "rb")
        payload = MIMEBase('application', 'octate-stream', Name=os.path.basename(pdf_file_path))
        payload.set_payload((pdf_file).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_file_path))

