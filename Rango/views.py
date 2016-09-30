from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from Rango.models import Category, Page
from Rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page,
#if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request):  #CORRECTION TODO
        return '/rango/'

"""
Note that it is not technically a view, because it does not return a response - it
is just a helper function

* Note that all cookie values are returned as strings;
"""

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits


def index(request):
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages':page_list}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'Rango/index.html', context=context_dict)
    return response

def about(request):
    context_dict={'visits':request.session['visits']}
    return render(request, 'Rango/about.html',context=context_dict)

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

@login_required
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


@login_required
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

"""
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                    'Rango/register.html',
                    {'user_form': user_form,
                     'profile_form': profile_form,
                     'registered': registered})
"""
"""
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                #Django method called reverse to obtain the URL of the Rango application.
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid Login details: {0},{1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'Rango/login.html', {})
"""

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

"""
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
"""
