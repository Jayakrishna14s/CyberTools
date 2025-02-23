from django.shortcuts import render # type: ignore
def index(request):
    return render(request, 'index.html', {})