from django.core.management.base import BaseCommand
from user.helpers import fill_cache


class Command(BaseCommand):

    def handle(self, *args, **options):
        fill_cache()
