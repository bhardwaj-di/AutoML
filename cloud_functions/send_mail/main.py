import email, smtplib, ssl
import fpdf

import firestore as fs

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendMail(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    resource_string = context.resource
    # print out the resource string that triggered the function
    print(f"Function triggered by change to: {resource_string}.")
    # now print out the entire event object
    print(str(event))
    
    def createPDF(data,document):
        pdf = fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for i,val in zip(data.keys(),data.values()):
            pdf.write(5,"Speaker "+str(i))
            pdf.ln()
            pdf.ln()
            pdf.write(5,str(val))
            pdf.ln()
            pdf.ln()
        pdf.output("/tmp/" + document+ ".pdf")

    def sendmail(document):
        subject = "An email with attachment from Python"
        body = "This is an email with attachment sent from Python"
        sender_email = "dspbigdata@gmail.com"
        receiver_email = "dspbigdata@gmail.com"
        password = "Bigdata@123"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = "/tmp/" + document+ ".pdf"  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
  
    document_name = resource_string.split("/")[-1]
    print("document name is",document_name)
    summarized_dict = fs.getData(document_name)
    print("summarized dict is",summarized_dict)
    createPDF(summarized_dict,document_name)
    sendmail(document_name)





