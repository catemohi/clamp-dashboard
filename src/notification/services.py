from json import dumps
from typing import Mapping

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


def notify_issue(issue: Mapping, *args, **kwargs):
    """Уведомление о новом обращении.
    """
    print(("issue_notifi", {"type": kwargs.get('type'),
                            "is_changed": kwargs.get('is_changed'),
                            "text": issue}))

    resilt = ("issue_notifi", {"type": kwargs.get('type'),
                               "is_changed": kwargs.get('is_changed'),
                               "text": dumps(issue)})

    async_to_sync(channel_layer.group_send)(resilt)
    return resilt
