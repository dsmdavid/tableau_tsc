from log import MyLogger

logger = MyLogger(log_file='logs.log', log_path='logs', name=__name__)
logger.debug('here and there')
for i in range(10):
    print(i)
    if i == 5:
        logger.warning(f'oh oh, we\'ve reached {i}')
def tester():
    logger.debug(f'inside TESTER {tester.__name__}')
tester()