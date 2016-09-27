from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'Rango/index.html', context=context_dict)

def about(request):
    return render(request, 'Rango/about.html')
