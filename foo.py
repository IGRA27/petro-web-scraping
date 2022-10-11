import logging 

logging.basicConfig(filename="log.txt", level = logging.DEBUG,
                    format="%(asctime)s %(message)s")
logging.info("Debug logging test..")
