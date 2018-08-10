import grader.pagination as pagination_lib

from grader import application, db
from grader.models import Problem
from grader.utilities import add_url_params

from flask import render_template, url_for, request

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

@application.route('/problems/trending')
def problems_trending():
    def url_func(page_num):
        return add_url_params(url_for('problems_trending'), {'page':page_num})

    query = get_problem_query()
    return render_template('problems_trending.html', **get_problems(query, url_func))

@application.route('/problems/alphabetical', defaults={'direction': 'az'})
@application.route('/problems/alphabetical/<direction>')
def problems_alphabetical(direction):
    query = get_problem_query()

    if direction == 'az':
        query = query.order_by(Problem.name)
    elif direction == 'za':
        query = query.order_by(Problem.name.desc())
    else:
        return redirect(url_for('problems_alphabetical'))

    def url_func(page_num):
        return add_url_params(url_for('problems_alphabetical', direction=direction), {'page':page_num})

    return render_template('problems_alphabetical.html', **get_problems(query, url_func), sorted_az=(direction == 'az'))

@application.route('/problems/difficulty')
def problems_difficulty():
    def url_func(page_num):
        return add_url_params(url_for('problems_difficulty'), {'page':page_num})

    query = get_problem_query()
    return render_template('problems_alphabetical.html', **get_problems(query, url_func))

@application.route('/problems/acceptance')
def problems_acceptance():
    def url_func(page_num):
        return add_url_params(url_for('problems_acceptance'), {'page':page_num})

    query = get_problem_query()
    return render_template('problems_alphabetical.html', **get_problems(query, url_func))

@application.route('/problems/completion')
def problems_completion():
    def url_func(page_num):
        return add_url_params(url_for('problems_completion'), {'page':page_num})

    query = get_problem_query()
    return render_template('problems_alphabetical.html', **get_problems(query, url_func))

@application.route('/problems')
def problems():
    return redirect(url_for('problems_trending'))