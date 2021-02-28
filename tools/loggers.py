import logging
from logging import handlers
from os import getcwd, path


log_lvl = logging.INFO

PAYMENT_INFO_LOGGER = logging.getLogger("payment_logger")
PAYMENT_INFO_LOGGER.setLevel(log_lvl)

# console_logger = logging.StreamHandler()
# console_logger.setLevel(log_lvl)
# console_logger.setFormatter(logging.Formatter(fmt='%(asctime)s: %(message)s'))
# payment_logger.addHandler(console_logger)

handler = handlers.RotatingFileHandler(path.join(getcwd(), "payments.log"), encoding='utf8', maxBytes=10 * 1024 * 1024)
handler.setLevel(log_lvl)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s: %(message)s'))
PAYMENT_INFO_LOGGER.addHandler(handler)

