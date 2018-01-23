# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm

def index(request):
    # Query the database for all currently stored categories sorted by the number of likes (descending)
    # Pick the 5 most liked categories, or all, if less than five
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Place the list of top liked categories to the context dictionary which will be handled to the template
    context_dict = {'categories': category_list,
                    'pages': page_list}

    # Return a response to the request, specifying the template file and the template context dictionary
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'Why don\'t you check out these sweet images?'}

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

def add_category(request):
    form = CategoryForm()

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

    # If the request is not POST, it is GET and we display
    # the appropriate template with the form
    return render(request, 'rango/add_category.html', {'form': form})

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

def register(request):
    # Determines whether the user registration has been successful
    registered = False


    # If we have a POST request, we need to process the form data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If both forms are valid, save the new user
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Hashing the password and updating the user object
            user.set_password(user.password)
            user.save()

            # Creating a profile for the user
            # Since we set attributes ourselves, commit=False
            # This delays saving the model until we are ready
            profile = profile_form.save(commit=False)
            profile.user = user

            # If the user provided a profile picture
            # link it to his profile
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            # User registration successful, update the variable
            registered = True

        else:
            # Invalid form(s) - print problems to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not POST, so we render the new user form using two ModelForm instnaces
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})








