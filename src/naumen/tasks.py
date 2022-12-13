from celery import shared_task
from logging import getLogger

from .services import crud_service_level
from .services import crud_mttr, crud_flr, download_issues
from .services import issues_list_synchronization
from .services import delete_trouble_ticket_model
from .services import create_or_update_trouble_ticket_model
from .exceptions import NaumenServiceError


LOGGER = getLogger(__name__)


# @shared_task
# def update_issues():
#     """Задача обновления обращений первой линии.

#     Returns:
#         bool: True
#     """
#     crud_issues(**{'parse_issues_cards': True})
#     return True


# @shared_task
# def update_vip_issues():
#     """Задача обновления обращений VIP линии.

#     Returns:
#         bool: True
#     """
#     crud_issues(**{'is_vip': True, 'parse_issues_cards': True})
#     return True


@shared_task
def update_service_level():
    """Функция обновления уровня SL
    """
    crud_service_level()
    return True


@shared_task
def update_mttr_level():
    """Функция обновления уровня MTTR
    """
    crud_mttr()
    return True


@shared_task
def update_flr_level():
    """Функция обновления уровня FLR
    """
    crud_flr()
    return True


@shared_task
def crud_issue(*args, **kwargs):
    issue = kwargs.get('issue')
    try:
        if kwargs.get('is_delete'):
            delete_trouble_ticket_model(issue.get('uuid'))
        else:
            create_or_update_trouble_ticket_model(issue)
    except NaumenServiceError as err:
            LOGGER.exception(err)


@shared_task
def update_issues(*args, **kwargs):
    """Задача для обновления обращений в базе данных
    """

    issues = download_issues(*args, **kwargs)
    kwargs["issues"] = issues
    new_issues, updated_issues, deleted_issues = \
        issues_list_synchronization(*args, **kwargs)
    new_issues = new_issues + updated_issues
    [crud_issue.delay(**{**kwargs, 'is_delete': True, 'issue': issue}) for issue in deleted_issues]
    [crud_issue.delay(**{**kwargs, 'is_delete': False, 'issue': issue}) for issue in new_issues]
    return True