#django imports
from django.http import HttpResponse
from django.shortcuts import render
#models imports
from Rango.models import Category, Page
#forms imports
from Rango.forms import CategoryForm, PageForm

def index(request):
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages':page_list}
    return render(request, 'Rango/index.html', context=context_dict)

def about(request):
    return render(request, 'Rango/about.html')

def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'Rango/category.html', context_dict)

"""
This is a Cross-Site
Request Forgery (CSRF) token, which helps to protect and secure the HTTP POST action
that is initiated on the subsequent submission of a form.
"""

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    return render(request, 'Rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                #page.views = 0 #TODO
                page.save()
                return show_category(request, category_name_slug)
        else:
            print form.errors

    context_dict = {'form':form, 'category': category}
    return render(request, 'Rango/add_page.html', context_dict)
