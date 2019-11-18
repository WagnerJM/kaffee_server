from lib.watcher import Watcher
import logging

logger = logging.getLogger(__name__)
def main():
    logging.debug("creating watcher")
    w = Watcher()
    logging.debug("running")
    w.run()


if __name__ == '__main__':
    main()
