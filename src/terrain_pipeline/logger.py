import logging
import os
import sys

def setup_logger(name: str = "GeoFlow", log_file: str = "system.log") -> logging.Logger:
    """
    Configures and returns a standardized logger outputting to both console and file.
    Fulfills the DEBUG, INFO, WARNING, ERROR requirements from the project design.
    """
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.DEBUG)
    
    # Standardized output format
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)-7s] [%(module)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console Handler: Outputs INFO and higher to the terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # File Handler: Outputs DEBUG and higher to a persistent log file
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, log_file)
    
    file_handler = logging.FileHandler(file_path, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger