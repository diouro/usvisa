import logging

logging.basicConfig(level=logging.INFO, filename="test.log", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")

logging.info("Test started....")

REPLACEWITH = 'test'
TEXT = f"this is a %s"

MODIFIED_TEXT = TEXT % REPLACEWITH

logging.info(MODIFIED_TEXT)

logging.info("Test finished!")