import configparser
from serialListener.listener import SerialListener
from lib.logger import log

def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    logging = log(config)
    logger = logging.getLogger(__name__)
    
    logger.info("Getting config settings [{}, {}, {}]".format(
        config.get("Default", "serial_port"),
        config.get("Default", "message_queue_host"),
        config.get("Default", "message_queue_port")
    ))
    serialListener = SerialListener(
        config.get("Default", "serial_port"),
        config.get("Default", "message_queue_host"),
        config.get("Default", "message_queue_port")
    )
    serialListener.listener_state = True
    serialListener.run()


if __name__ == "__main__":
    main()