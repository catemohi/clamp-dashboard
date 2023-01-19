from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

from naumen.services import get_issues_from_db
from notification.services import get_notification
from notification.services import get_burned_notification_setting
from notification.services import get_returned_notification_setting

from .services import get_day_dates_and_data, json_encoding, get_load_ratings
from .services import issues_on_group, get_load_naumen_settings, get_day_report


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


def index_page(request):
    url = reverse_lazy('login')
    return redirect(url)


def login_page(request):
    """Функция обрабатывающая вход пользователей.

    Args:
        request (_type_): запрос
    """
    context = {}

    if request.method != 'POST':
        return render(request, 'dashboard/login.html', context=context)

    data = request.POST
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is None:
        login(request, username, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('dashboard')

    return render(request, 'dashboard/login.html', context=context)


def logout_page(request):
    """Функция обрабатывающая выход пользователей.

    Args:
        request (_type_): запрос
    """
    logout(request)
    return redirect('login')


def dashboard_page(request):
    context = {}
    # Запрос данных для контекста
    returned_notification_settings = get_returned_notification_setting()
    burned_notification_settings = get_burned_notification_setting()
    names = get_load_naumen_settings()
    ratings = get_load_ratings()
    day_dict = get_day_dates_and_data()
    notifications = get_notification(slice=50, json_type=True)
    issues_count = issues_on_group()

    context.update(day_dict)
    context.update(
        {'returned_notification_settings': returned_notification_settings})
    context.update(
        {'burned_notification_settings': burned_notification_settings})
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications, "ratings": ratings})
    context.update({**issues_count, 'names': names})
    return render(request, 'dashboard/dashboard.html', context=context)


def table_page(request):
    context = {}
    # Запрос данных для контекста
    returned_notification_settings = get_returned_notification_setting()
    burned_notification_settings = get_burned_notification_setting()
    names = get_load_naumen_settings()
    ratings = get_load_ratings()
    day_dict = get_day_dates_and_data()
    notifications = get_notification(slice=50, json_type=True)
    issues_count = issues_on_group()

    context.update(day_dict)
    context.update(
        {'returned_notification_settings': returned_notification_settings})
    context.update(
        {'burned_notification_settings': burned_notification_settings})
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications, "ratings": ratings})
    context.update({**issues_count, 'names': names})
    return render(request, 'dashboard/table.html', context=context)


def reports_page(request):
    context = {}
    # Запрос данных для контекста
    returned_notification_settings = get_returned_notification_setting()
    burned_notification_settings = get_burned_notification_setting()
    ratings = get_load_ratings()
    names = get_load_naumen_settings()
    day_dict = get_day_dates_and_data()
    notifications = get_notification(slice=50, json_type=True)
    issues_count = issues_on_group()

    context.update(day_dict)
    context.update(
        {'returned_notification_settings': returned_notification_settings})
    context.update(
        {'burned_notification_settings': burned_notification_settings})
    context.update(theme_check(request.COOKIES))
    context.update({'notifications': notifications, "ratings": ratings})
    context.update({**issues_count, 'names': names})
    return render(request, 'dashboard/reports.html', context=context)


def dashboard_json(request):
    data = request.POST
    day_dict = get_day_dates_and_data(data['date'])
    day_dict['dashboard_data'] = json_encoding(day_dict['dashboard_data'])
    day_dict['dates'] = json_encoding(day_dict['dates'])
    return JsonResponse(day_dict)


def report_json(request):
    data = request.POST
    day_dict = get_day_report(data['desired_date'], data['comparison_date'])
    day_dict['desired_date'] = json_encoding(day_dict['desired_date'])
    day_dict['comparison_date'] = json_encoding(day_dict['comparison_date'])
    return JsonResponse(day_dict)


def table_json(request):
    content = get_issues_from_db()
    return JsonResponse({'data': content})
