import os
import logging
# Set up logging configuration
def setup_logging(log_path):
    os.makedirs(log_path, exist_ok=True)
    logging.basicConfig(
        filename=f"{log_path}/log.out",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging

# Create the output folder if it doesn't exist
def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)