from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .forms import UserForm,SendForm
from .parser import parse
 
def index(request):
    userform = UserForm()
    send_file = SendForm()
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