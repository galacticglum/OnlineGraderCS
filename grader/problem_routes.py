import grader.pagination as pagination_lib

from grader import application, db
from grader.models import Problem
from grader.utilities import add_url_params

from flask import render_template, url_for, request, redirect

def get_problem_query():
    return db.session.query(Problem).filter(~Problem.contests.any())

def get_problems(query, url_func):
    """
    Get paginated problems from a query.

    :param query: the query to get the problems from
    :param url_func: a function to compute the target url from a page number.
    :return: a dictionary containing the pagination entries and paginated problems.

    >> get_problems(query, lambda page_num: f'path.com/?page={page_num}')
    >> {'pagination_entries': [...], 'problems': [...]}
    """

    page = request.args.get('page', default=1, type=int)
    if page < 1:
        return redirect(url_func(1))

    all_problems = query.all()
    max_page = pagination_lib.get_max_page(len(all_problems))

    if page > max_page:
        return redirect(url_func(max_page))

    pagination_entries, items_on_page = pagination_lib.paginate(all_problems, page, url_func)
    return {'pagination_entries' : pagination_entries, 'problems' : items_on_page }

@application.route('/problems/')
def problems_no_category():
    return redirect(url_for('problems', sort_category='trending'))

@application.route('/problems/<sort_category>/')
def problems(sort_category):
    def url_func(page_num):
        return add_url_params(url_for('problems', sort_category=sort_category), {**request.args, 'page': page_num})

    sort_direction = request.args.get('sort_direction', type=int)
    query = get_problem_query()

    if sort_category == 'trending':
        pass
    elif sort_category == 'alphabetical':
        # Sort a-z
        if sort_direction != 0:
            query = query.order_by(Problem.name)
        # Sort z-a
        else:
            query = query.order_by(Problem.name.desc())
    elif sort_category == 'difficulty':
        if sort_direction != 0:
            query = query.order_by(Problem.difficulty)
        else:
            query = query.order_by(Problem.difficulty.desc())
    else:
        return redirect(url_for('problems_no_category'))

    template_name = f'problems/problems_{sort_category}.html'
    sort_direction_zero_url = add_url_params(request.url, {'sort_direction': 0})
    sort_direction_one_url = add_url_params(request.url, {'sort_direction': 1})

    return render_template(template_name, **get_problems(query, url_func), sort_direction=sort_direction, \
        sort_direction_zero_url=sort_direction_zero_url, sort_direction_one_url=sort_direction_one_url)