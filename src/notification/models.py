from django.db import models


class StepNotificationSetting(models.Model):

    """
    Модель свойств и настроек для уведомлений событий по группе.
    """
    name = models.CharField(
        max_length=100, verbose_name='Название',
        )
    step = models.CharField(
        max_length=100, verbose_name='Шаг',
        )
    step_time = models.IntegerField(
        default=0, verbose_name='Время отработки на шаге (сек.)',
        db_index=True,
        )
    alarm_time = models.IntegerField(
        default=0,
        verbose_name='Время до лимита до которое предупредить (сек.)',
        db_index=True,
        )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('step',)
        verbose_name = 'Настроки уведомлений шага'
        verbose_name_plural = 'Настроки уведомлений шагов'


class RetrunToWorkNotificationSetting(models.Model):

    """
    Модель свойств и настроек для уведомлений для обращений
    возращаемых с отложенного шага.
    """
    name = models.CharField(
        max_length=100, verbose_name='Название',
        )
    step = models.CharField(
        max_length=100, verbose_name='Шаг',
        )
    alarm_time = models.IntegerField(
        default=0,
        verbose_name='Время до возврата за которое предупредить (сек.)',
        db_index=True,
        )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('step',)
        verbose_name = 'Настроки уведомлений возвращения'
        verbose_name_plural = 'Настроки уведомлений возвращения'
