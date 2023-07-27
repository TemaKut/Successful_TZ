from collections import defaultdict

from rest_framework.exceptions import NotFound
from rest_framework import status
from django.db.models.query import QuerySet
from django.db.models import Count

from sales.models import File


class TopFiveCustomers():
    """ Манипуляции для получения топ 5 покупателей из конкретного csv в БД """

    def __init__(self, filename: str):
        """ Инициализация объекта """
        self.filename: str = filename

    def get_top_five(self) -> dict:
        """ Получить топ 5 пользователей из объекта файла """
        file: File = self._get_file_from_db()
        deals: QuerySet = file.deals.get_queryset()

        five_with_spent: QuerySet = self._get_top_five_names_by_spent(deals)

        return self._add_gems(five_with_spent, deals)

    def _add_gems(self, five_with_spent: QuerySet, deals: QuerySet) -> dict:
        """ Добавить общие камни для покупателей. """
        # На этом шаге объединим результирующую информацию с камнями в словарь
        result: list[dict] = []

        # Разложим queryset в словарь и добавим уникальные камни к каждому
        for one in five_with_spent:
            customer: str = one.get('customer')
            spent: int = one.get('spent')
            _items: QuerySet = deals.filter(customer=customer)\
                .values_list('item', flat=True)\
                .distinct()

            gems: list[str] = list(_items)

            result.append({'customer': customer, 'spent': spent, 'gems': gems})

        # Совместим все камни в словарь, где посчитаем их количество
        count_gem: defaultdict = defaultdict(int)

        for one in result:

            for gem in one.get('gems'):
                count_gem[gem] += 1

        # Удалим из уникальных камней те, что встречаются меньше двух раз
        for one_index, one in enumerate(result):

            for gem_index, gem in enumerate(one.get('gems')):

                if count_gem[gem] < 2:
                    del result[one_index]['gems'][gem_index]

        return result

    def _get_top_five_names_by_spent(self, deals: QuerySet) -> list[str]:
        """ Получить 5 имён, чьи траты больше всех. """
        result: QuerySet = deals.values('customer')\
            .annotate(spent=Count('total'))\
            .order_by('-spent')[:5]

        return result

    def _get_file_from_db(self) -> File:
        """ Получить модель файла из БД """
        file: File = File.objects.filter(name=self.filename).first()

        if not file:
            raise NotFound('No filename', status.HTTP_404_NOT_FOUND)

        return file
