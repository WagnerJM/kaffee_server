import pika
import redis
import configparser
from sqlalchemy import create_engine

from lib import log

config = configparser.ConfigParser()
config.read("config.ini")
logging = log(config)
logger = logging.getLogger(__name__)
#TODO: initiate sqlalchemy connection
engine = create_engine(sqlite:///../../app.db)

#TODO: enable redis connection
r = redis.Redis()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    logger.info(" [x] Received %r" % body)
    #TODO: if yes: get coffee_count, coffee_count += 1, save to redis, 
    logger.debug(f"checking if {body} exists")
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