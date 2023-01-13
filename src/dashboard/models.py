from django.db import models


class NaumenSetting(models.Model):

    """
    Модель необходимых настроек для работы парсера.
    """
    name = models.CharField(
        verbose_name='Название', max_length=120,
        default='Настройки для парсера Naumen',
        )
    first_group_name = models.CharField(
        max_length=150,
        verbose_name='Наименование первой линии в Naumen',
        default='Группа поддержки и управления сетью  (Напр ТП В2В)',
        )
    vip_group_name = models.CharField(
        max_length=150,
        verbose_name='Наименование VIP линии в Naumen',
        default='Группа поддержки VIP - клиентов (Напр ТП В2В)',
        )
    general_group_name = models.CharField(
        max_length=150,
        verbose_name='Наименование общих показателей в Naumen',
        default='Итог',
        )
    step_name_on_group = models.CharField(
        max_length=150,
        verbose_name='Наименование шага "на группе" в Naumen',
        default='передано в работу (напр тех под В2В)',
        )
    step_name_on_worker = models.CharField(
        max_length=150,
        verbose_name='Наименование шага "на сотруднике" в Naumen',
        default='принято в работу',
        )
    is_active = models.BooleanField(default=False,
                                    verbose_name='Активные настройки')

    def __str__(self):
        return f'{self.name} №{self.id}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Настройки для парсера Naumen'
        verbose_name_plural = 'Настройки для парсера Naumen'
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['is_active'],
                condition=models.constraints.Q(is_active=True),
                name='Активные настройки')
        ]


class RatingSetting(models.Model):

    """
    Модель необходимых настроек для работы аналитики.
    """
    name = models.CharField(
        verbose_name='Название', max_length=120,
        default='Настройки для создания аналитики',
        )
    service_level = models.IntegerField(
        verbose_name='Нижняя граница допустимого SL (%)',
        default=80,
        )
    mttr_level = models.IntegerField(
        verbose_name='Верхняя граница допустимого MTTR (мин.)',
        default=45,
        )
    flr_level = models.IntegerField(
        verbose_name='Нижняя граница допустимого FLR (%)',
        default=30,
        )
    num_issues_first_line = models.IntegerField(
        verbose_name='Норма количества обращений первой линии (кол.)',
        default=180,
        )
    num_issues_vip_line = models.IntegerField(
        verbose_name='Норма количества обращений VIP линии (кол.)',
        default=60,
        )
    num_issues_general = models.IntegerField(
        verbose_name='Норма количества обращений общее (кол.)',
        default=240,
        )
    num_issues_closed = models.IntegerField(
        verbose_name='Норма количества закрытых обращений (кол.)',
        default=75,
        )
    num_issues_general = models.IntegerField(
        verbose_name='Норма количества первичных обращений (кол.)',
        default=60,
        )
    is_active = models.BooleanField(default=False,
                                    verbose_name='Активные настройки')

    def __str__(self):
        return f'{self.name} №{self.id}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Настройки аналитики'
        verbose_name_plural = 'Настройки аналитики'
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['is_active'],
                condition=models.constraints.Q(is_active=True),
                name='Активные настройки')
        ]
