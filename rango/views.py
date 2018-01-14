# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Dictionary of Django template variable values
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return a response to the request, specifying the template file and the template context dictionary
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'Why don\'t you check out these sweet images?'}

    return render(request, 'rango/about.html', context=context_dict)