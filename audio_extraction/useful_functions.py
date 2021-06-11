# useful_functions.py

# Packages
from datetime import datetime
from pathlib import Path
import logging


# Function that sets up the logging system
def set_up_logging(log_path = "logging/", log_level = logging.WARNING):
    """
    Sets the logging configuration and writes log files to the specified path.

    Arguments:
    log_path | str
    The path to the directory where you want to write log files to.
    
    log_level | int
    How much detail the log file should include. See link for more details:
    https://docs.python.org/3/howto/logging.html#when-to-use-logging
    These are the relevant levels in increasing order:
    logging.DEBUG, logging.INFO, logging.WARNING
    
    Example:
    set_up_logging(log_path = "logging/", log_level = logging.DEBUG)
    """
    # Make the chosen directory if it doesn't already exist
    Path(log_path).mkdir(exist_ok = True)
    # Use the current time to create the log file name
    current_time = datetime.now().strftime("%Y-%m-%d_%HH%MM")
    log_filename = current_time + ".log"
    # Set up the log file
    logging.basicConfig(filename = Path(log_path, log_filename),
                        level = log_level,
                        filemode = "a") # Can append to existing file
    