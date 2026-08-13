from django.shortcuts import render
def home(request):
    return render(request, 'UI/Home.html')
def about(request):
    return render(request, 'UI/About.html')

# Create your views here.
def home(request):
    return render(request, 'UI/Home.html')
