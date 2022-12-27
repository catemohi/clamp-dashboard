from logging import getLogger

from .services import crud_service_level, parse_issue_card
from .services import crud_mttr, crud_flr, download_issues
from .services import issues_list_synchronization
from .services import delete_trouble_ticket_model
from .services import create_or_update_trouble_ticket_model
from .services import get_issues_from_db
from .services import check_issue_return_timers, check_issue_deadline
from .exceptions import NaumenServiceError
from .services import create_or_update_trouble_ticket_model
from .services import crud_flr, crud_mttr, download_issues
from .services import crud_service_level, parse_issue_card
from .services import delete_trouble_ticket_model
from .services import issues_list_synchronization


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
            delete_trouble_ticket_model(issue)
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
    crud_issues, deleted_issues = \
        issues_list_synchronization(*args, **kwargs)
    [crud_issue.delay(**{**kwargs, 'is_delete': True, 'issue': issue})
     for issue in deleted_issues]
    [crud_issue.delay(**{**kwargs, 'is_delete': False, 'issue': issue})
     for issue in crud_issues]
    return True


@shared_task
def check_issue_deadline_and_timer(issue: dict, *args, **kwargs):
    """Задача проверки времени отработки и таймера возврата в работу обращения

    Args:
        issue (dict): обращение которое необходимо проверить
    """
    check_issue_deadline(issue, *args, **kwargs)
    check_issue_return_timers(issue, *args, **kwargs)


@shared_task
def check_issues_deadline_and_timer(*args, **kwargs):
    """Задача для проверки времени отработки и таймера возврата в работу
    обращений
    """
    issues = get_issues_from_db(*args, **kwargs)

    for issue in issues:
        check_issue_deadline_and_timer.delay(issue, *args, **kwargs)
