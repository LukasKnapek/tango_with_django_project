# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.webhose_search import run_query


def index(request):
    request.session.set_test_cookie()
    # Query the database for all currently stored categories sorted by the number of likes (descending)
    # Pick the 5 most liked categories, or all, if less than five
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Place the list of top liked categories to the context dictionary which will be handled to the template
    context_dict = {'categories': category_list,
                    'pages': page_list,}

    # Obtain Response object early, so we can add cookie information
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context_dict)

    # Return the response, with its cookies updated
    return response

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    visitor_cookie_handler(request)
    context_dict = {'boldmessage': 'Why don\'t you check out these sweet images?',
                    'visits': request.session['visits']}

    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    # Try to match and fetch a category using the slug
    try:
        # Throws DoesNotExist exception if there is no category with the slug
        category = Category.objects.get(slug=category_name_slug)

        # Get all pages associated with the category
        pages = Page.objects.filter(category=category)

        # Store them in context dict for rendering in template
        context_dict['pages'] = pages
        # Als store the category itself in the dict. We can then verify in template whether we fetched it or not
        context_dict['category'] = category
    except Category.DoesNotExist:
        # If there is no category with the slug, pass along empty context dict
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    context_dict = {}

    # Is the request POST, i.e. has the user submitted the form?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # We only save the form if it is valid, otherwise
        # print out errors in terminal
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    context_dict["form"] = form
    print(type(context_dict))

    # If the request is not POST, it is GET and we display
    # the appropriate template with the form
    return render(request, 'rango/add_category.html', context_dict)

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    # Is the request POST, i.e. has the user submitted the form?
    if request.method == 'POST':
        form = PageForm(request.POST)

        # We only save the form if it is valid, otherwise
        # print out errors in terminal
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    # If the request is not POST, it is GET and we display
    # the appropriate template with the form
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {'logged_user': request.user.username})

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get the number of visits to the site
    # If the cookie exists, the value returned is casted to int
    # Otherwise, default value of 1 is used
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    # Get the last visit datetime, if the cookie exists
    # Otherwise, set the last visit datetime to now
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    print (request.session)
    request.session['visits'] = visits

def search(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list, 'query': query})

