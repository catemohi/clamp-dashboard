from datetime import datetime
from json import dumps

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from naumen.services import get_issues_from_db
from notification.services import get_notify

from .services import convert_datestr_to_datetime_obj, get_params, get_dashboard_data, analytics, get_date_collections, json_encoding


def theme_check(cookies):
    """Переключатель темы на основе данных из cookies

    Args:
        cookies (_type_): куки пользователя

    Returns:
        dict: калассы которые необходимо навесить на DOM дерево
    """

    theme = cookies.get('theme')

    if theme == 'dark':
        return {'body_class': 'dark-theme-var',
                'theme_toggler_dark': 'active',
                'theme_toggler_white': ''}

    return {'body_class': '',
            'theme_toggler_dark': '',
            'theme_toggler_white': 'active'}


def index(request):
    url = reverse_lazy('dashboard')
    return redirect(url)


def dashboard(request):
    context = {}
    # Запрос данных для контекста
    today = datetime.now()
    dates = get_date_collections(today.strftime('%Y-%m-%d'))
    dashboard_data = get_dashboard_data(dates.chosen_date.strftime('%Y-%m-%d'))
    before_day_data = get_dashboard_data(dates.before_day.strftime('%Y-%m-%d'))
    dashboard_data = analytics(dashboard_data, before_day_data)
    notifications = get_notify(slice=50)

    context.update({'dates': dates, 'dashboard_data': dashboard_data})
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications})
    context.update(
        {'trouble_ticket_counter': '99+', 'trouble_ticket_vip_counter': '99+'})
    return render(request, 'dashboard/dashboard.html', context=context)


def table(request):
    context = {}
    today = datetime.now()
    dates = get_date_collections(today.strftime('%Y-%m-%d'))
    dashboard_data = get_dashboard_data(dates.chosen_date.strftime('%Y-%m-%d'))
    before_day_data = get_dashboard_data(dates.before_day.strftime('%Y-%m-%d'))
    dashboard_data = analytics(dashboard_data, before_day_data)
    notifications = get_notify(slice=50)

    context.update({'dates': dates, 'dashboard_data': dashboard_data})
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications})
    context.update(
        {'trouble_ticket_counter': '99+', 'trouble_ticket_vip_counter': '99+'})
    return render(request, 'dashboard/table.html', context=context)


def reports(request):
    context = {}
    today = datetime.now()
    dates = get_date_collections(today.strftime('%Y-%m-%d'))
    dashboard_data = get_dashboard_data(dates.chosen_date.strftime('%Y-%m-%d'))
    before_day_data = get_dashboard_data(dates.before_day.strftime('%Y-%m-%d'))
    dashboard_data = analytics(dashboard_data, before_day_data)
    notifications = get_notify(slice=50)

    context.update({'dates': dates, 'dashboard_data': dashboard_data})
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications})
    context.update(
        {'trouble_ticket_counter': '99+', 'trouble_ticket_vip_counter': '99+'})
    return render(request, 'dashboard/reports.html', context=context)


def dashboard_json_data(request):
    data = request.POST
    dates = get_date_collections(data['date'])
    dashboard_data = get_dashboard_data(dates.chosen_date.strftime('%Y-%m-%d'))
    before_day_data = get_dashboard_data(dates.before_day.strftime('%Y-%m-%d'))
    dashboard_data = analytics(dashboard_data, before_day_data)
    dashboard_data = json_encoding(dashboard_data)
    dates = json_encoding(dates)
    responce = {"dashboard_data": dashboard_data, "dates": dates}

    return JsonResponse(responce)


def table_json_data(request):
    content = get_issues_from_db()
    return JsonResponse({'data': content})


def table_counter_json_data(request):
    content = len(get_issues_from_db())
    return JsonResponse({'data': content})


def log(request):
    context = {}
    notifications = get_notify(slice=50)
    context.update({'notifications': notifications})
    context.update(theme_check(request.COOKIES))
    return render(request, 'dashboard/log.html', context)


# def report_json_data(request):
#     data = request.POST
#     print(data)
#     desired_date = get_date_obj(data['desired_date'])
#     comparison_date = get_date_obj(data['comparison_date'])
#     content = get_day_params_and_analytics(desired_date, comparison_date)
#     return JsonResponse({'data': content})
