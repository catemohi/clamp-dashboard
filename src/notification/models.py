from django.db import models


class StepNotificationSetting(models.Model):

    """
    Модель свойств и настроек для уведомлений событий по группе.
    """

    steps = models.CharField(
        max_length=100, verbose_name='Шаг',
        )
    step_time = models.IntegerField(
        default=0, verbose_name='Время отработки на шаге (сек.)',
        db_index=True,
        )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('steps',)
        verbose_name = 'Настроки уведомлений шага'
        verbose_name_plural = 'Настроки уведомлений шагов'
