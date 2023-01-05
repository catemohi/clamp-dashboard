from datetime import datetime
from json import loads

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from naumen.services import get_issues_from_db
from notification.services import get_notify

from .services import convert_datestr_to_datetime_obj, get_params, get_dashboard_data, get_day_dates_and_data, analytics, get_date_collections, json_encoding, get_load_ratings, issues_on_group


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
    ratings = get_load_ratings()
    day_dict = get_day_dates_and_data()
    notifications = get_notify(slice=50)
    issues_count = issues_on_group()

    context.update(day_dict)
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications, "ratings": ratings})
    context.update(issues_count)
    return render(request, 'dashboard/dashboard.html', context=context)


def table(request):
    context = {}
    ratings = get_load_ratings()
    day_dict = get_day_dates_and_data()
    notifications = get_notify(slice=50)
    issues_count = issues_on_group()

    context.update(day_dict)
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications, "ratings": ratings})
    context.update(issues_count)
    return render(request, 'dashboard/table.html', context=context)


def reports(request):
    context = {}
    ratings = get_load_ratings()
    day_dict = get_day_dates_and_data()
    notifications = get_notify(slice=50)
    issues_count = issues_on_group()

    context.update(day_dict)
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications, "ratings": ratings})
    context.update(issues_count)
    return render(request, 'dashboard/reports.html', context=context)


def dashboard_json_data(request):
    data = request.POST
    day_dict = get_day_dates_and_data(data['date'])
    day_dict['dashboard_data'] = json_encoding(day_dict['dashboard_data'])
    day_dict['dates'] = json_encoding(day_dict['dates'])

    return JsonResponse(day_dict)


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
