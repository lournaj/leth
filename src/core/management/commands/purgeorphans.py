from django.core.management.base import BaseCommand, CommandError
from core.models import Feed, Article


class Command(BaseCommand):
    help = 'Remove articles and feeds which have no subscriptions'

    def add_arguments(self, parser):
        parser.add_argument('--feeds',
                            action='store_true',
                            dest='feeds',
                            default=False,
                            help='Delete orphan feeds')
        parser.add_argument('--articles',
                            action='store_true',
                            dest='articles',
                            default=False,
                            help='Delete orphan articles')

    def handle(self, *args, **options):
        if not options['feeds'] and not options['articles']:
            raise CommandError('You must specify at least one entity to purge')
        if options['feeds']:
            deleted, _ = Feed.objects.filter(
                subscribers__isnull=True,
                article__isnull=True).delete()
            self.stdout.write('{} feeds deleted'.format(deleted))
        if options['articles']:
            deleted, _ = Article.objects.filter(
                subscribers__isnull=True).delete()
            self.stdout.write('{} articles deleted'.format(deleted))
