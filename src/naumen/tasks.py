from celery import shared_task
from .services import crud_issues, crud_service_level
from .services import crud_mttr, crud_flr, download_issues


@shared_task
def update_issues():
    """Задача обновления обращений первой линии.

    Returns:
        bool: True
    """
    crud_issues(**{'parse_issues_cards': True})
    return True


@shared_task
def update_vip_issues():
    """Задача обновления обращений VIP линии.

    Returns:
        bool: True
    """
    crud_issues(**{'is_vip': True, 'parse_issues_cards': True})
    return True


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

def _crud_issue(*args, )

@shared_task
def update_issues(*args, **kwargs):
    """Задача для обновления обращений в базе данных
    """
    issues = download_issues(*args, **kwargs)


