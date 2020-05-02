import logging
from datetime import date,datetime

import SSH_Constant as sc


def get_time():
    return datetime.strftime(datetime.now(),'%m-%d-%Y_%I-%M')


def logformat(f):
    FORMAT = '%(asctime)s %(message)s '
    logging.basicConfig(filename=f, level=logging.DEBUG, format=FORMAT, datefmt='%m-%d-%Y %I:%M:%S %p')


def logfilegen():
    # Generates file name Dyanamically
    file_name = sc.AUTOMATION_LOGS_LOC + "\%s" % str(get_time()) + ".log"
    return file_name


def info(message):
    logging.info(" INFO:: " + message)


def warning(message):
    logging.warning(" WARINING:: " + message)


def error(message):
    logging.error(" ERROR:: " + message)


def critical(message):
    logging.critical(" CRITICAL:: " + message)

def debug(message):
    logging.debug("Debug:: "+message)