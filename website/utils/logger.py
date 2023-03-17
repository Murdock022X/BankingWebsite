import logging
import json

# Load in the loggin configuration.
config = {}
with open('app_config.json') as cf:
    config = json.load(cf)

# Create the logging configuration to log things, set file, level of log, and format.
logging.basicConfig(filename=config['LOGFILE'],
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def log_general(*args):
    """
    Allow you to log a general piece of information.
    """        
    res = "Log Info: "
    for arg in args:
        res += arg
        res += ' '

    logging.info(res)

