import logging


def log_and_execute(log_message, func, *args, **kwargs):
    logging.info(log_message)
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(f"Error during {log_message.lower()}: {e}")
        return None