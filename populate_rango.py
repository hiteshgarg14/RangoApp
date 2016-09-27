import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','RangoApp.settings')

#django.setup() to import your Django projects settings.
import django
django.setup()

from Rango.models import Category, Page

def populate():
    python_pages = [
        {"title": "Official Python Tutorial",
        "url":"http://docs.python.org/2/tutorial/",
        "views":100},
        {"title":"How to Think like a Computer Scientist",
        "url":"http://www.greenteapress.com/thinkpython/",
        "views":50},
        {"title":"Learn Python in 10 Minutes",
        "url":"http://www.korokithakis.net/tutorials/python/",
        "views":25} ]

    django_pages = [
        {"title":"Official Django Tutorial",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
        "views":200},
        {"title":"Django Rocks",
        "url":"http://www.djangorocks.com/",
        "views":100},
        {"title":"How to Tango with Django",
        "url":"http://www.tangowithdjango.com/",
        "views":50} ]

    other_pages = [
        {"title":"Bottle",
        "url":"http://bottlepy.org/docs/dev/",
        "views":400},
        {"title":"Flask",
        "url":"http://flask.pocoo.org",
        "views":200} ]

    cats = {"Python": {"pages": python_pages,
                        "views":128,
                        "likes":64},
        "Django": {"pages": django_pages,
                    "views":64,
                    "likes":32},
        "Other Frameworks": {"pages": other_pages,
                             "views":32,
                             "likes":16} }

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

"""
we can
use get_or_create() to check if the entry exists in the database for us. If it does not exist,
the method creates it. It does, then a reference to the specific model instance is returned.
"""
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()

"""
The __name__ == '__main__' trick is a useful one that allows a Python module to act as
either a reusable module or a standalone Python script.
"""
