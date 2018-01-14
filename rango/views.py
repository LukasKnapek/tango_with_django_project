# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    response = """Rango says hey there partner! </br>
                    Perhaps you would like to check the <a href="/rango/about/">About page</a>?"""
    return HttpResponse(response)

def about(request):
    response = """Rango says this here is the about page! </br>
                    There ain't much yet, maybe you're better off going back to the <a href="/rango/">main page</a>?"""
    return HttpResponse(response)