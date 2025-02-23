from django.shortcuts import render # type: ignore
def manual(request):
    return render(request, 'manual.html', {})