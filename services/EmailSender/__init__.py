 import logging

def log(config):

    logger_dict = {
        "1": logging.DEBUG,
        "2": logging.INFO,
        "3": logging.WARNING,
        "4": logging.ERROR
    }

    logger_lvl = logger_dict.get(config.get("Logger", "level"))

    logging.basicConfig(level=logger_lvl, filename="../logs/{}.log".format(config.get("Logger", "name")), format='%(asctime)s %(levelname)s:%(message)s')
    return logging
