from enum import Enum

from bs4 import BeautifulSoup
from bs4 import Tag


class EmptyChecker(Enum):
    empty = 1
    non_empty = 2


def empty_tag(tag: Tag) -> bool:
    """checks emptiness"""
    if tag and tag.text.strip():
        return False  # non-empty
    return True  # empty


def check_tags(tags: Tag) -> EmptyChecker:
    if tags:
        validator = sum([empty_tag(t) for t in tags])
        if validator == len(tags):  # page is all empty
            return EmptyChecker.empty
        else:
            return EmptyChecker.non_empty
    else:
        return EmptyChecker.empty


def empty_page(tag: Tag) -> bool:
    p_tags = tag.find_all('p')  # can be zero p tags
    div_tags = tag.find_all('div')

    if (not div_tags) and (not p_tags):
        return True

    p_tags_checker = check_tags(p_tags)
    div_tags_checker = check_tags(div_tags)

    p_condition = p_tags_checker == EmptyChecker.empty
    div_condition = div_tags_checker == EmptyChecker.empty

    if p_condition and div_condition:
        return True  # EmptyChecker.empty
    return False  # EmptyChecker.non_empty


def scanned_document(document: BeautifulSoup) -> bool:
    pages = document.find_all('div', {'class': 'page'})
    empty_pages = sum(empty_page(page) for page in pages)

    # title page always not empty. condition for shorter documents
    all_empty_but_first = (empty_pages >= len(pages) - 1)
    empty_threshold = (empty_pages > 5)

    if all_empty_but_first or empty_threshold:
        return True
    return False
