import wikipediaapi
import concurrent.futures
from tqdm import tqdm
from time import sleep
import src.config as config


def get_subcategories(category, depth, max_depth, output=None):
    '''
    Get the subcategories of a given category
    :param category: wikipediaapi.WikipediaPage
    :param depth: int (current depth, starts at 0)
    :param max_depth: int (maximum depth to search)
    :param output: file object (to write the subcategories to a file)
    :return: list of subcategories
    '''
    if depth > max_depth:
        return []
    subcategories = []

    for i in range(3):
        try:
            cats = category.categorymembers.values()
            break
        except Exception as e:
            sleep(3)
            
    for subcategory in cats:
        if subcategory.ns == wikipediaapi.Namespace.CATEGORY:
            cat_name = ':'.join(subcategory.title.split(":")[1:])
            subcategories.append(cat_name)
            if output is not None:
                # print("Writing to file")
                output.write(f"{cat_name}\n")
            subcategories.extend(get_subcategories(subcategory, depth + 1, max_depth))

    return subcategories

def get_articles(category, articles_set):
    articles = []
    for member in category.categorymembers.values():
        if member.ns == wikipediaapi.Namespace.MAIN:
            if member.title not in articles_set:
                articles.append(member)
                articles_set.add(member.title)
    return articles

def fetch_subcategories(subcategory):
    return get_subcategories(subcategory, config.MIN_DEPTH, config.MAX_DEPTH)