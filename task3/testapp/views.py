from django.shortcuts import render
from django.http import HttpResponse

from .utils import UserForm,SendForm,parse

def index(request):
    userform = UserForm()
    if request.method == "POST":
        link = request.POST.get("link")
        login = request.POST.get("login")
        password = request.POST.get("password")
        semester_range = range(int(request.POST.get("first_semester")),int(request.POST.get("last_semester")))
        table = parse(link,login,password,semester_range)
        response = HttpResponse(table, content_type='csv')
        response['Content-Disposition'] = f'attachment; filename="table.csv"'
        return response
    else:
        return render(request, "index.html", {"form": userform})