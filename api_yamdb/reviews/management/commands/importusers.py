import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = ('Imports users from a csv file. In django settings,'
            'specify the absolute path'
            'PATH_IMPORT_CSV to the directory with csv files.'
            'Example -  PATH_IMPORT_CSV = "api_yamdb/static/data/"')

    def add_arguments(self, parser):
        parser.add_argument(
            '-file', type=str,
            help='csv file name - (for example.csv)')

    def handle(self, *args, **options):
        file = options['-file']
        with open(f'{settings.PATH_IMPORT_CSV}{file}') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_create = User.objects.get_or_create(
                    email=row['email'],
                    username=row['username'])
                if user_create[1]:
                    print(f"{user_create} - user was created successfully")
                else:
                    print(f"{user_create} - this user already exists")
