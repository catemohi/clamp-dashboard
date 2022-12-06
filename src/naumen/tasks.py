from celery import shared_task
from .services import crud_issues,crud_service_level,crud_mttr,crud_flr

@shared_task
def update_issues():
    crud_issues()
    return True