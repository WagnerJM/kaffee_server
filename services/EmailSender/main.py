import pika
import smtplib
import configparser
from Email import EmailMessage
from sqlalchemy import create_engine
from lib import log


config = configparser.ConfigParser()
config.read("config.ini")

logging = log(config)
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    logger.info(" [x] Received %r" % body)
    email = EmailMessage()
    email["Subject"] = "Kaffee Rechnung"
    email["From"] = config.get("Email", "email")
    email["To"] = body["email"]

    #TODO: get email body from database
    email_body = """ """
    email.set_content("email_body")
    s = smtplib.SMTP(host=settings.smtp_host, port=int(settings.smtp_port))
    """
    if settings['email_tls']:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(settings.system_email, settings.email_password)
        s.send_message(email)
        s.quit()
    else:
        s.ehlo()
        s.login(settings.system_email, settings.email_password)
        s.send_message(email)
        s.quit()
    """
  

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue=config.get("Email", "queue"))
    channel.basic_consume(
        queue=config.get("Email","queue"), on_message_callback=callback, auto_ack=True
        )
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()