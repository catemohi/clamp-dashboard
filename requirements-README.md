### channels-redis

Due to an upstream bug (linked below), we see `RuntimeError: Event loop is closed` errors with newer versions of `channels-redis`.
Upstream is aware of the bug and it is likely to be fixed in the next release according to the issue linked below.
For now, we pin to the old version, 3.4.1

* https://github.com/django/channels_redis/issues/332
* https://github.com/ansible/awx/issues/13313

