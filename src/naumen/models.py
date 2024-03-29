from datetime import timedelta

from django.db import models


class Issue(models.Model):

    """
    Модель обращения
    """

    uuid = models.CharField(
        primary_key=True, max_length=100,
        verbose_name='Идентификатор обращения',
        )
    url_issue = models.CharField(
        default="#", max_length=150,
        verbose_name='Ссылка на обращение',
        )
    number = models.CharField(
        max_length=50, verbose_name='Номер',
        )
    name = models.CharField(
        max_length=250, verbose_name='Название',
        )
    issue_type = models.CharField(
        max_length=100, verbose_name='Тип обращения',
        )
    step = models.CharField(
        max_length=100, verbose_name='Шаг',
        )
    step_time = models.IntegerField(
        default=0, verbose_name='Время шага (сек.)', db_index=True,
        )
    responsible = models.CharField(
        max_length=150, verbose_name='Ответственный за шаг')
    last_edit_time = models.DateTimeField(
        auto_now=False, auto_now_add=False,
        verbose_name=('Последнее изменение состояния'), db_index=True,
        )
    vip_contragent = models.BooleanField(
        default=False, verbose_name='VIP статус контрагента')
    creation_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, verbose_name='Дата создания',
        )
    uuid_service = models.CharField(
        max_length=200, null=True, verbose_name='Идентификатор услуги',
        )
    name_service = models.TextField(
        null=True, verbose_name='Услуги',
        )
    url_service = models.CharField(
        default="#", max_length=150,
        verbose_name='Ссылка на контрагента',
        )
    uuid_contragent = models.CharField(
        max_length=200, null=True, verbose_name='Идентификатор контрагента',
        )
    name_contragent = models.CharField(
        max_length=200, null=True, verbose_name='Контрагент',
        )
    url_contragent = models.CharField(
        default="#", max_length=150,
        verbose_name='Ссылка на контрагента',
        )
    return_to_work_time = models.DateTimeField(
        auto_now=False, null=True, auto_now_add=False,
        verbose_name='Время возврата в работу',
        )
    description = models.TextField(null=True,
                                   verbose_name='Описание обращения',
                                   )
    alarm_return_to_work = models.BooleanField(
        default=False, verbose_name='Статус уведомление о возврате в работу',
    )
    alarm_deadline = models.BooleanField(
        default=False,
        verbose_name='Статус уведомление привышении лимита',
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('last_edit_time',)
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'


class ServiceLevelReport(models.Model):

    """
    Модель отчёта SL
    """

    date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='Дата', db_index=True)
    name_group = models.CharField(
        max_length=60, verbose_name='Группа', db_index=True,
        )
    total_number_trouble_ticket = models.IntegerField(
        verbose_name='Поступило обращений в ТП', db_index=True,
        )
    number_primary_trouble_tickets = models.IntegerField(
        verbose_name='Количество первичных обращений',
        )
    number_of_trouble_ticket_taken_before_deadline = models.IntegerField(
        verbose_name='Принято до крайнего срока',
        )
    number_of_trouble_ticket_taken_after_deadline = models.IntegerField(
        verbose_name='Принято после крайнего срока',
        )
    service_level = models.FloatField(
        verbose_name='Service Level(%)', db_index=True,
        )

    class Meta:
        ordering = ('date',)
        verbose_name = 'SL report'
        verbose_name_plural = 'SL reports'

    def __str__(self):
        return f'{self.date} {self.name_group}'


class MeanTimeToResponseReport(models.Model):

    """
    Модель отчёта MTTR
    """

    date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='Дата', db_index=True,
        )
    total_number_trouble_ticket = models.IntegerField(
        verbose_name='Всего обращений', db_index=True,
        )
    average_mttr = models.DurationField(
        default=timedelta(0, 0), verbose_name='Средн МТТР',
        )
    average_mttr_tech_support = models.DurationField(
        default=timedelta(0, 0), verbose_name='Средн МТТР ТП',
        )

    class Meta:
        ordering = ('date',)
        verbose_name = 'MTTR report'
        verbose_name_plural = 'MTTR reports'

    def __str__(self):
        return f'{self.date}'


class FlrReport(models.Model):

    """
    Модель отчёта FLR
    """

    date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='Дата', db_index=True,
        )
    flr_level = models.FloatField(
        verbose_name='FLR по дн (в %)', db_index=True,
        )
    number_trouble_ticket_closed_independently = models.IntegerField(
        verbose_name='Закрыто обращений без других отделов',
        )
    number_primary_trouble_tickets = models.IntegerField(
        verbose_name='Количество первичных обращений',
        )

    class Meta:
        ordering = ('date',)
        verbose_name = 'FLR report'
        verbose_name_plural = 'FLR reports'

    def __str__(self):
        return f'{self.date}'


class AhtReport(models.Model):

    """
    Модель отчёта AHT
    """

    date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='Дата', db_index=True,
        )
    segment = models.CharField(
        verbose_name="Сегмент", max_length=100, db_index=True,
    )
    aht_level = models.FloatField(
        verbose_name='Среднее время', db_index=True,
        )
    issues_received = models.IntegerField(
        verbose_name='Поступило обращений', db_index=True,
        )

    class Meta:
        ordering = ('date',)
        verbose_name = 'AHT report'
        verbose_name_plural = 'AHT reports'

    def __str__(self):
        return f'{self.date}'


class WorkdayRate(models.Model):

    """
    Модель показателей.
    """

    name = models.CharField(
        max_length=60, default="Безымянный", verbose_name='Название',
        db_index=True,
        )
    service_level = models.FloatField(
        verbose_name='Service Level(%)', default=0.0, db_index=True,
        )
    average_mttr_tech_support = models.DurationField(
        default=timedelta(0, 0), verbose_name='Средн МТТР ТП',
        )
    flr_level = models.FloatField(
        verbose_name='FLR по дн (в %)', default=0.0, db_index=True,
        )
    num_issues_first_line = models.IntegerField(
        verbose_name='Дневная норма обращений первой линии', db_index=True,
        )
    num_issues_vip_line = models.IntegerField(
        verbose_name='Дневная норма обращений vip линии', db_index=True,
        )
    num_issues_general = models.IntegerField(
        verbose_name='Дневная норма обращений на все линии', db_index=True,
        )
    num_issues_closed = models.IntegerField(
        verbose_name='Количество закрытых обращений', db_index=True,
        )
    num_primary_issues = models.IntegerField(
        verbose_name='Количество первичных обращений',
        )

    class Meta:
        verbose_name = 'Норма'
        verbose_name_plural = 'Нормы'

    def __str__(self):
        return self.name
