from functools import lru_cache

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from sales.utils.save import SaveCSVToDB
from sales.utils.get_top import TopFiveCustomers


@api_view(['POST'])
def csv_save(request):
    """ Эндпоинт сохранения .csv файла в БД. """
    to_db: SaveCSVToDB = SaveCSVToDB()
    to_db.save(request.FILES)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@lru_cache()  # Кэширование
def top_5_customers(request, filename: str):
    """ Вывести топ 5 покупателей из конкретного .csv """
    top_5: TopFiveCustomers = TopFiveCustomers(filename)

    return Response(top_5.get_top_five(), status=status.HTTP_200_OK)
