from django.core.management.base import BaseCommand
from django.utils import timezone


from scrape_games.models import MyCacheTable

class Command(BaseCommand):
    help = 'Clears expired cache pages from database'

    def handle(self, *args, **options):
        expired_pages = [page for page in MyCacheTable.objects.all() if page.expires < timezone.now()]
        i = 0
        for page in expired_pages:
            page.delete()
            i+=1
            self.stdout.write('Removed expired cached page:'+str(i))
        self.stdout.write('Done.')

