from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator


class File(models.Model):
    """ БД модель файла данных. """

    name = name = models.CharField(
        verbose_name='Название файла',
        unique=True,
        null=False,
        blank=False,
        max_length=150,
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        """ Строчное представление. """

        return f'{self.__class__.__name__}<{self.name}>'


class Deal(models.Model):
    """ БД модель сделки (продажи) """

    customer = models.CharField(
        verbose_name='Имя покупателя',
        null=False,
        blank=False,
        max_length=150,
        validators=[MinLengthValidator(1)],
    )
    item = models.CharField(
        verbose_name='Название камня',
        null=False,
        blank=False,
        max_length=150,
        validators=[MinLengthValidator(1)],
    )
    total = models.PositiveIntegerField(
        verbose_name='Сумма сделки',
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара',
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
    )
    date = models.DateTimeField(
        verbose_name='Дата и время сделки',
        null=False,
        blank=False,
    )
    file = models.ForeignKey(
        verbose_name='Файл',
        to=File,
        on_delete=models.CASCADE,
        related_name='deals',
    )

    class Meta:
        ordering = ['-customer']
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        """ Строчное представление. """

        return f'{self.__class__.__name__}<{self.customer}>'
