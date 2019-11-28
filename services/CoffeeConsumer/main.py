import pika
import os
import redis
import configparser
import sqlite3

from lib import log

config = configparser.ConfigParser()
config.read("config.ini")
logging = log(config)
logger = logging.getLogger(__name__)
#TODO: enable redis connection
r = redis.Redis()
conn = sqlite3.connect(os.path.join(os.getenv("HOME"), "app.db")
c = conn.cursor()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    logger.info(" [x] Received %r" % body)
    #TODO: if yes: get coffee_count, coffee_count += 1, save to redis, 
    logger.debug(f"checking if {body} exists")
    c.execute(f"SELECT coffee_count from users where key_ID='{body}'")
    user = c.fetchone()
    new_coffee_count = user[0] + 1
    c.execute(f"UPDATE users SET coffee_count='{new_coffee_count}' WHERE key_ID='{body}'")
    conn.commit()
    conn.close()
    """
    if r.exists(body):
        logger.debug(f"{body} was found")
        logger.info(f"Getting coffee_count for {body}")
        coffee_count = r.get(body)
        logger.info(f"coffee_count for {body} is {coffee_count}")
        coffee_count += 1
        logger.debug("increasing coffee_count by 1")
        try:
            r.set(body, coffee_count)
            logger.info(f"new coffee_count for {body}:{coffee_count} in cache")
        except:
            logger.error("An error occured while saving coffee_count to cache")
        #TODO: save to db
    """
    #TODO: if not: get coffee_count for key coffee_count += 1 save to redis, save to db
    






def main():
   
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='newCoffee')
    channel.basic_consume(
        queue='newCoffee', on_message_callback=callback, auto_ack=True
        )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()
