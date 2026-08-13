from django.shortcuts import render
def home(request):
    return render(request, 'UI/Home.html')
def about(request):
    return render(request, 'UI/About.html')

<<<<<<< HEAD
=======
# Create your views here.
def home(request):
    return render(request, 'UI/Home.html')
>>>>>>> 38a8c9f563335d1275bdb4442475e9d22be50e85
