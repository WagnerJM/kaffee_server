import os
import serial 
import pika
from lib.logger import logging
import time



class SerialListener:

    def __init__(self, serial_port, msgQ_host, msgQ_port):
        self.logger = logging.getLogger(__name__)
        self.listener_state = False
       
        try:
            self.con = serial.Serial(serial_port)
            self.logger.debug("Initializing serial connection on {}".format(serial_port))
        
        except Exception as e:
            self.logger.error("No serial connection")
            self.logger.error(e)
        
        try:
            self.logger.debug("Initializing message queue connection")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        except Exception as e:
            self.logger.error("No message queue connection")
            self.logger.error(e)

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="newCoffee")
    
    def run(self):
        if not self.con.is_open:
            self.con.open()
        key_list = []
        try:
            binary_key = self.con.readline()
            self.con.close()
            key = binary_key.decode("utf-8")
            key = key.rstrip()
            self.logger.info(f"Sending {key}")
                    
            self.channel.basic_publish(
                        exchange='', 
                        routing_key='newCoffee', 
                        body=key
                    )
            time.sleep(5)
            print("Restarting connection")
            self.run()

        except serial.SerialException:
            print("Restarting connection")
            self.run()

        """
        while self.listener_state:
            key_list = []
            key_list.append(self.con.readline())

            key_list = []
            binary_key = self.con.readline()
            if binary_key:

                key = binary_key.decode("utf-8")
                key = key.rstrip()
                key_list.append(key)
                key_set = set(key_list)
                if len(key_set) == 1:
                    key_id = next(iter(key_set))
                    #TODO: send key_id to redditMQ
                    self.logger.info(f"Sending {key_id}")
                    self.channel.basic_publish(
                        exchange='', 
                        routing_key='newCoffee', 
                        body=key_id
                    )
        """

            

