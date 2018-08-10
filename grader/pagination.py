from math import ceil
from flask import url_for
from enum import Enum

MAX_PAGINATION_ENTRIES = 7
ITEMS_PER_PAGE = 20

class PaginationState(Enum):
    enabled = 0
    disabled = 1
    active = 2

    def to_html_str(self):
        if self == PaginationState.enabled:
            return ''
        
        if self == PaginationState.disabled:
            return 'disabled'

        if self == PaginationState.active:
            return 'active'

class PaginationEntry(object):
    def __init__(self, value, state, href):
        self.state = state
        self.value = value
        self.href = href

def get_url_with_page(route, page_num):
    return url_for(route) + f'?page={page_num}'

def get_max_page(items_len):
    return ceil(items_len / ITEMS_PER_PAGE)

def paginate(items, page_num):
    if items == None or len(items) == 0: return None, None

    max_page = get_max_page(len(items))
    items_on_page = items[ITEMS_PER_PAGE * (page_num - 1):ITEMS_PER_PAGE * page_num]
    if max_page <= MAX_PAGINATION_ENTRIES:
        prev_pagination_entry = PaginationEntry('«', 
                                                PaginationState.disabled if page_num == 1 else PaginationState.enabled, 
                                                get_url_with_page('problems', page_num - 1))

        entries = [prev_pagination_entry]

        for i in range(1, max_page + 1):
            entry = PaginationEntry(i, 
                    PaginationState.active if i == page_num else PaginationState.enabled, 
                    get_url_with_page('problems', i))

            entries.append(entry)

        next_pagination_entry = PaginationEntry('»', 
                                                PaginationState.disabled if page_num == max_page else PaginationState.enabled, 
                                                get_url_with_page('problems', page_num + 1))
        entries.append(next_pagination_entry)

        return entries, items_on_page


    