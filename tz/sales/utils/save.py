import csv

from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.utils import IntegrityError

from sales.models import Deal, File


class SaveCSVToDB():
    """ Манипуляции для сохранения csv файла в Базу Данных. """

    def save(self, files: Request.FILES) -> None:
        """ Сохранить файл в БД. """
        file: InMemoryUploadedFile = self._validate_files(files)

        file_model: File = File(name=file.name)
        deal_models: list[Deal] = []

        for row in csv.DictReader(file.read().decode().splitlines()):
            deal_models.append(
                Deal(
                    customer=row.get('customer'),
                    item=row.get('item'),
                    total=row.get('total'),
                    quantity=row.get('quantity'),
                    date=row.get('date'),
                    file=file_model,
                )
            )

        try:
            file_model.save()

        except IntegrityError:
            raise ValidationError('This file was uploaded.')

        except Exception as e:
            raise ValidationError(f'Error with File <{e}>')

        try:
            Deal.objects.bulk_create(deal_models)

        except Exception as e:
            raise ValidationError(f'Error with Deal <{e}>')

    def _validate_files(self, files: Request.FILES) -> InMemoryUploadedFile:
        """ Провалидировать переданные файлы на количество == 1 и .csv """

        if len(files) == 0:

            raise ValidationError('No files to save.')

        if len(files) > 1:

            raise ValidationError('Too many files to save.')

        for file in files.values():

            if not file.name.endswith('.csv'):

                raise ValidationError('Extantion is not .csv')

            return file
