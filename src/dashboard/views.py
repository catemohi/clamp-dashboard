from unicodedata import name
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .services import *
from django.http import JsonResponse


# Create your views here.
def theme_check(cookies):
    theme = cookies.get('theme')
    if theme == 'dark':
        return {'body_class': 'dark-theme-var', 'theme_toggler_dark': 'active', 'theme_toggler_white': ''}
    return {'body_class': '', 'theme_toggler_dark': '', 'theme_toggler_white': 'active'}


def index(request):
    # data = get_today_data()
    url = reverse_lazy('dashboard')
    return redirect(url)

  
def dashboard(request):
    context = {}
    context.update(theme_check(request.COOKIES))
    context.update({'trouble_ticket_counter': get_trouble_ticket_count_from_db()})
    return render(request,'dashboard/dashboard.html', context=context)


def table(request):
    context = {}
    context.update(theme_check(request.COOKIES))
    context.update({'trouble_ticket_counter': get_trouble_ticket_count_from_db()})
    return render(request,'dashboard/table.html', context=context)


def reports(request):
    context = {}
    context.update(theme_check(request.COOKIES))
    context.update({'trouble_ticket_counter': get_trouble_ticket_count_from_db()})
    return render(request,'dashboard/reports.html', context=context)


def dashboard_json_data(request):
    data = request.POST
    date_obj = get_date_obj(data['date'])
    params_dict = get_params(date_obj)
    return JsonResponse(params_dict)


def table_json_data(request):
    data = request.POST
    content = get_trouble_ticket_collection_from_db()
    return JsonResponse({'data': content})


def table_counter_json_data(request):
    data = request.POST
    content = get_trouble_ticket_count_from_db()
    return JsonResponse({'data': content})


def report_json_data(request):
    data = request.POST
    print(data)
    desired_date = get_date_obj(data['desired_date'])
    comparison_date = get_date_obj(data['comparison_date'])
    content = get_day_params_and_analytics(desired_date, comparison_date)
    return JsonResponse({'data': content})


def test(request):
    update_issues.delay()
    return HttpResponse('ok')