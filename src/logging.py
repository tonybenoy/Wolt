import logging


def get_logger(name, level=logging.DEBUG) -> logging.Logger:
    FORMAT = (
        "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s()"
        + " -%(asctime)s]\n\t %(message)s \n"
    )
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    logging.basicConfig(format=FORMAT, datefmt=TIME_FORMAT, level=level)

    logger = logging.getLogger(name)
    return logger
