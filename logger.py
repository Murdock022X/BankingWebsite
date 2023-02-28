import logging
import json

config = {}
with open('app_config.json') as cf:
    config = json.load(cf)

logging.basicConfig(filename=config['LOGFILE'],
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

class Logger():

    def log_general(self, *args):
        res = "Log Info: "
        for arg in args:
            res += arg
            res += ' '

        logging.info(res)

    def executed(self, line):
        logging.info(line)

