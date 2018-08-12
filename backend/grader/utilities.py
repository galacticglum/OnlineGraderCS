from flask import abort, jsonify

def check_none(**kwargs):
    """
    Checks whether the specified keyword argument values are None.

    :param kwargs: the objects to check.::

    :returns: A list containing the names of the objects which are None.
    """

    nones = []
    for key in kwargs:
        if kwargs[key] is None: nones.append(key)

    return nones

def list_join(list, conjunction_str, format_func=str, oxford_comma=True):
    """
    Joins a list in grammatically-correct fashion.

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
    comma = ',' if oxford_comma else ''

    return f'{first_part}{oxford_comma} {conjunction_str} {format_func(list[-1])}'

def stdio_confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

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

def error_response(status_code, message):
    abort(jsonify(status_code=status_code, message=message))

def check_for_missing_params(**kwargs):
    empty_params = check_none(**kwargs)
    if len(empty_params) == 0: return
    
    is_plural = len(empty_params) > 1
    conjunction_word = 'are' if is_plural  else 'is'
    s_ending = 's' if is_plural else ''

    missing_param_left = list_join(empty_params, 'and', lambda x: f'\'{x}\'')
    error_message = f'{missing_param_left} parameter{s_ending} {conjunction_word} missing.'
    error_response(400, message=error_message)