from json import dumps
from typing import Mapping


def notify_issue(issue: Mapping, *args, **kwargs):
    """Уведомление о новом обращении.
    """
    print(("issue_notifi", {"type": kwargs.get('type'),
                            "is_changed": kwargs.get('is_changed'),
                            "text": issue}))
    resilt = ("issue_notifi", {"type": kwargs.get('type'),
                               "is_changed": kwargs.get('is_changed'),
                               "text": dumps(issue)})
    return resilt
