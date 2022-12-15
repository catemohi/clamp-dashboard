from celery import shared_task
from logging import getLogger

from .services import crud_service_level, parse_issue_card
from .services import crud_mttr, crud_flr, download_issues
from .services import issues_list_synchronization
from .services import delete_trouble_ticket_model
from .services import create_or_update_trouble_ticket_model
from .exceptions import NaumenServiceError


LOGGER = getLogger(__name__)


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
            issue = parse_issue_card(issue)
            create_or_update_trouble_ticket_model(issue)
    except NaumenServiceError as err:
            LOGGER.exception(err)


@shared_task
def update_issues(*args, **kwargs):
    """Задача для обновления обращений в базе данных
    """

    issues = download_issues(*args, **kwargs)
    kwargs["issues"] = issues
    new_issues, unioned_issues, deleted_issues = \
        issues_list_synchronization(*args, **kwargs)
    deep_parsed_issues = new_issues + unioned_issues
    [crud_issue.delay(**{**kwargs, 'is_delete': True, 'issue': issue}) for issue in deleted_issues]
    [crud_issue.delay(**{**kwargs, 'is_delete': False, 'issue': issue}) for issue in deep_parsed_issues]
    return True