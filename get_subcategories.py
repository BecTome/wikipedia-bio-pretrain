import wikipediaapi
from tqdm import tqdm
import concurrent.futures
from datetime import datetime
import os
import logging
import traceback

from src import config
from src.retrieve import fetch_subcategories
from src.utils import setup_logging, create_output_folder

timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
log_folder = config.LOG_FOLDER
output_folder_name = config.OUTPUT_FOLDER
log_output = os.path.join(log_folder, "subcategories", timestamp)


def main():
    logging = setup_logging(log_path=log_output)
    lan = "es"

    output_folder = os.path.join(output_folder_name, "subcategories", lan, timestamp)
    create_output_folder(output_folder)
    
    output_file = os.path.join(output_folder, f"subcategories_{lan}.txt")
    
    wiki = wikipediaapi.Wikipedia(config.AGENT, lan)
    category = wiki.page(config.D_LANG_CAT[lan])
    logging.info(f"Get subcategories from Category: {category.title}")
    
    # with open(output_file, "a") as output:
    #     output.write(f"{category.title}\n")
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_subcategories, subcategory)
            for subcategory in category.categorymembers.values()
            if subcategory.ns == wikipediaapi.Namespace.CATEGORY
        ]
        
        subcategories = []
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            try:
                subcategories.extend(future.result())
            except Exception as e:
                logging.error(f"Error fetching subcategories: {e}")

    with open(output_file, "a") as output:
        for subcategory in subcategories:
                output.write(f"{subcategory}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        filename = datetime.now().strftime('%d%m%Y_%H%M%S')
        with open(f"{log_output}/log.err", "w") as f:
            traceback.print_exc(file=f)
