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

def make_entry_for_page(current_page_num, page_num, url):
    state = PaginationState.active if page_num == current_page_num else PaginationState.enabled
    return PaginationEntry(page_num, state, url)

def paginate(items, page_num):
    if items == None or len(items) == 0: return None, None

    max_page = get_max_page(len(items))
    items_on_page = items[ITEMS_PER_PAGE * (page_num - 1):ITEMS_PER_PAGE * page_num]
    
    super_prev_pagination_state = PaginationState.disabled if page_num <= 5 else PaginationState.enabled
    super_prev_pagination_entry = PaginationEntry('<i class="fas fa-angle-double-left"></i>', super_prev_pagination_state,  
                                                    get_url_with_page('problems', page_num - 5))

    prev_pagination_state = PaginationState.disabled if page_num == 1 else PaginationState.enabled
    prev_pagination_entry = PaginationEntry('<i class="fas fa-angle-left"></i>', prev_pagination_state,  get_url_with_page('problems', page_num - 1))

    entries = [super_prev_pagination_entry, prev_pagination_entry]

    ELLPSIS_ENTRY = PaginationEntry('…', PaginationState.disabled, '')

    if max_page <= MAX_PAGINATION_ENTRIES:
        for i in range(1, max_page + 1):
            entries.append(make_entry_for_page(page_num, i, get_url_with_page('problems', i)))
    else:
        entries.append(make_entry_for_page(page_num, 1, get_url_with_page('problems', 1)))
        if page_num > 4:
            entries.append(ELLPSIS_ENTRY)

            if page_num < max_page - 4:
                entries.append(make_entry_for_page(page_num, page_num - 1, get_url_with_page('problems', page_num - 1)))
                entries.append(make_entry_for_page(page_num, page_num, get_url_with_page('problems', page_num)))
                entries.append(make_entry_for_page(page_num, page_num + 1, get_url_with_page('problems', page_num + 1)))
                entries.append(ELLPSIS_ENTRY)
            else:
                for i in range(4, 0, -1):
                    page = max_page - i
                    entries.append(make_entry_for_page(page_num, page, get_url_with_page('problems', page)))
        else:
            for i in range(2, 7):
                entries.append(make_entry_for_page(page_num, i, get_url_with_page('problems', i)))

            entries.append(ELLPSIS_ENTRY)

        entries.append(make_entry_for_page(page_num, max_page, get_url_with_page('problems', max_page)))
        

    next_pagination_state = PaginationState.disabled if page_num == max_page else PaginationState.enabled
    next_pagination_entry = PaginationEntry('<i class="fas fa-angle-right"></i>', next_pagination_state, get_url_with_page('problems', page_num + 1))

    super_next_pagination_state = PaginationState.disabled if page_num + 5 > max_page else PaginationState.enabled
    super_next_pagination_entry = PaginationEntry('<i class="fas fa-angle-double-right"></i>', super_next_pagination_state, 
                                                    get_url_with_page('problems', page_num + 5))

    entries.append(next_pagination_entry) 
    entries.append(super_next_pagination_entry) 

    return entries, items_on_page



    