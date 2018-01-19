import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

    # Lists of dictionaries containing pages that will be added to categories
    python_pages = [{"title": "Official Python Tutorial", "url": "http://docs.python.org/2/tutorial/",
                     "view": 10000},
                    {"title": "How to Think like a Computer Scientist", "url": "http://www.greenteapress.com/thinkpython/",
                     "view": 9999},
                    {"title": "Learn Python in 10 Minutes", "url": "http://www.korokithakis.net/tutorials/python/",
                     "view": 1224}]

    django_pages = [{"title": "Official Django Tutorial", "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
                     "view": 102},
                    {"title": "Django Rocks", "url": "http://www.djangorocks.com/",
                     "view": 4190},
                    {"title": "How to Tango with Django", "url": "http://www.tangowithdjango.com/",
                     "view": 122}]

    other_pages = [{"title": "Bottle", "url": "http://bottlepy.org/docs/dev",
                    "view": 90},
                    {"title": "Flask", "url": "http://flask.pocoo.org",
                     "view": 95}]

    # Categories dictionary
    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}}

    # Go through the categories dictionary, create the categories and add all of their pages to them
    for cat, cat_data in cats.iteritems():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["view"])

    # Print out all categories and their pages
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

# get_or_create returns a tuple (object, created) where the first element is a reference to the created/fetched object
# and the second element specifies whether a new object was created
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()


