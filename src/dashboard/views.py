from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from naumen.services import get_issues_from_db

from .services import convert_datestr_to_datetime_obj, get_params


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
    context.update(theme_check(request.COOKIES))
    context.update(
        {'trouble_ticket_counter': '99+', 'trouble_ticket_vip_counter': '99+'})
    return render(request, 'dashboard/dashboard.html', context=context)


def table(request):
    context = {}
    context.update(theme_check(request.COOKIES))
    context.update(
        {'trouble_ticket_counter': '99+', 'trouble_ticket_vip_counter': '99+'})
    return render(request, 'dashboard/table.html', context=context)


def reports(request):
    context = {}
    context.update(theme_check(request.COOKIES))
    context.update(
        {'trouble_ticket_counter': '99+', 'trouble_ticket_vip_counter': '99+'})
    return render(request, 'dashboard/reports.html', context=context)


def dashboard_json_data(request):
    data = request.POST
    datetime_obj = convert_datestr_to_datetime_obj(data['date'])
    params_dict = get_params(datetime_obj)
    return JsonResponse(params_dict)


def table_json_data(request):
    content = get_issues_from_db()
    return JsonResponse({'data': content})


def table_counter_json_data(request):
    content = len(get_issues_from_db())
    return JsonResponse({'data': content})


def log(request):
    context = {}
    context.update(theme_check(request.COOKIES))
    return render(request, 'dashboard/log.html', context=context)

# def report_json_data(request):
#     data = request.POST
#     print(data)
#     desired_date = get_date_obj(data['desired_date'])
#     comparison_date = get_date_obj(data['comparison_date'])
#     content = get_day_params_and_analytics(desired_date, comparison_date)
#     return JsonResponse({'data': content})
