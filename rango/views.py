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
    response = """Rango says this here is the about page! </br>
                    There ain't much yet, maybe you're better off going back to the <a href="/rango/">main page</a>?"""
    return HttpResponse(response)