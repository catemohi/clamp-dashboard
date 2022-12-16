from typing import Mapping

from json import dumps
from .models import StepNotificationSetting


def notify_issue(issue: Mapping, notifi_type: str):
    """Уведомление о новом обращении.
    """
    resilt = ("issue_notifi", {"type": notifi_type, "text": dumps(issue)})
    print(resilt)
    return resilt