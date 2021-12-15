import time 

from django.db import connections
from django.db import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    '''Django command to pause execution until data base is available'''
    def handle(self, *args,**options):
        self.stdout.write('waiting for database...')
        db_con=None
        while not db_con:
            try:
                db_con= connections['default']
            except OperationalError:
                self.stdout.write('Databas unavailable, waiitng 1 second')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Database Available!'))
