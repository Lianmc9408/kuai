from django.shortcuts import render
from four import models

# Create your views here.
def index(request):
    result = models.MVinfo.objects.all()
    return render(request, "index.html", {'result': result})
