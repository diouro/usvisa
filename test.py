import logging
import time

logging.basicConfig(level=logging.INFO, filename="test.log", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")

logging.info("Test started....")

# REPLACEWITH = 'test'
# TEXT = f"this is a %s"
# MODIFIED_TEXT = TEXT % REPLACEWITH
# logging.info(MODIFIED_TEXT)

# REPLACEWITHDOUBLE = 'again'
# TEXT_DOUBLE = f"this is a %s %s"
# MODIFIED_TEXT_DOUBLE = TEXT_DOUBLE % (REPLACEWITH,REPLACEWITHDOUBLE)
# logging.info(MODIFIED_TEXT_DOUBLE)

# logging.info("Test finished!")
# logging.info("Test one '" + MODIFIED_TEXT + "' Test two '" + MODIFIED_TEXT_DOUBLE + "'")

# FIDS = [55,59]
# for f in FIDS:
#     logging.info(f)
#     time.sleep(5)

# SPEAK
# import os
# FACILITY_IDS = [(55, 'Rio de Janeiro'),(56, 'Sao Paulo'),(57,'Recife'),(128, 'Port Alegre')]
# INFINITE = 1
# while INFINITE:
#     for k,f in FACILITY_IDS:
#         os.system('say ' + f"There is a new schedule available in the facility %s at %s " % (k,f))
#         time.sleep(0.5)