import wikipediaapi
import concurrent.futures
from tqdm import tqdm

def get_subcategories(category, depth, max_depth):
    if depth > max_depth:
        return []
    subcategories = []
    for subcategory in category.categorymembers.values():
        if subcategory.ns == wikipediaapi.Namespace.CATEGORY:
            subcategories.append(subcategory)
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