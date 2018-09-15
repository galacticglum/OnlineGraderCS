def check_none(**kwargs):
    """
    Checks whether the specified keyword argument values are None.

    :param kwargs:
        the objects to check.

    :returns:
        A list containing the names of the objects which are None.
    """

    return list(filter(lambda x: kwargs[x] == None, kwargs.keys()))

def list_join(list, conjunction_str, format_func=str, oxford_comma=True):
    """
    Joins a list in a grammatically-correct fashion.

    :param list:
        the list to join.
    :param conjunction_str: 
        the string to use as conjunction between two items.
    :param format_func:
        a function that takes in a string and returns a formatted string (default=str, optional).
    :param oxford_comma: 
        indicates whether to use oxford comma styling (default=True, optional).
    :returns:
        a string representing the grammatically-correct joined list.

    :usage::
        >>> list_join(['apple', 'orange', 'pear'], 'and')
        apple, orange and pear'`
    """

    if not list: return ''
    if len(list) == 1: return format_func(list[0])
    
    first_part = ', '.join([format_func(i) for i in list[:-1]])
    comma = ',' if oxford_comma and len(list) > 2 else ''

    return f'{first_part}{comma} {conjunction_str} {format_func(list[-1])}'

def stdio_confirm(prompt=None, resp=False):
    """
    Prompts for yes or no response from the user. 
    
    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    :returns:
    True for yes and False for no.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

def setattr_not_none(obj, field_name, value):
    if not value: return
    setattr(obj, field_name, value)