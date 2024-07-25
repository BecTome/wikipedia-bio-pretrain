import wikipediaapi
from tqdm import tqdm
import concurrent.futures
from datetime import datetime
import os
import logging
import traceback

from src import config
from src.retrieve import fetch_articles, get_page_text_without_sections
from src.utils import setup_logging, create_output_folder

timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
log_folder = config.LOG_FOLDER
output_folder_name = config.OUTPUT_FOLDER
log_output = os.path.join(log_folder, "articles", timestamp)


def main():
    logging = setup_logging(log_path=log_output)
    lan = "es"

    output_folder = os.path.join(output_folder_name, "articles", lan, timestamp)
    create_output_folder(output_folder)
    
    output_file = os.path.join(output_folder, f"articles_{lan}.txt")
    
    wiki = wikipediaapi.Wikipedia(config.AGENT, lan)
    with open(config.CATEGORIES_FILE, "r") as f:
        categories = f.readlines()
    categories = [category.strip("\n") for category in categories]

    # with open(output_file, "a") as output:
    #     output.write(f"{category.title}\n")
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_articles, category, wiki)
            for category in categories
        ]
        
        articles = set()
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            try:
                articles = articles.union(future.result())
            except Exception as e:
                logging.error(f"Error fetching article: {e}")

    with open(output_file, "a") as output:
        for article in list(articles):
                try:
                    url = article.fullurl
                except:
                    url = f"https://{lan}.wikipedia.org/wiki/{article.title.replace(' ', '_')}"
                text = get_page_text_without_sections(article)
                # format <doc id="1" url="https://ca.wikipedia.org/wiki?curid=1" title="Àbac">
                output.write(f"<doc id=\"{article.pageid}\" url=\"{url}\" title=\"{article.title}\">\n{text}\n</doc>\n")

    # url_output_file = output_file.replace(f"articles_{lan}.txt", f"url_articles_{lan}.txt")
    # with open(url_output_file, "a") as output:
    #     for article in list(articles):
    #             try:
    #                 url = article.fullurl
    #             except:
    #                 url = f"https://{lan}.wikipedia.org/wiki/{article.title.replace(' ', '_')}"
    
    #             output.write(f"{url}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        filename = datetime.now().strftime('%d%m%Y_%H%M%S')
        with open(f"{log_output}/log.err", "w") as f:
            traceback.print_exc(file=f)
