from django.shortcuts import render
from django.http import HttpResponse

from naumen.tasks import update_issues

# Create your views here.
def test(request):
    update_issues.delay()
    return HttpResponse('ok')