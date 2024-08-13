import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = "dtrn hgca sllt pqmz"
SENDER = "adeiyeprecious650@gmail.com"
RECEIVER = "adeiyeprecious650@gmail.com"
def send_email(Image_path):
    print("send email has ended")
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer")

    with open(Image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(None,content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(Image_path="Images/16.png")
