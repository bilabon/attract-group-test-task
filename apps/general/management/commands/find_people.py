# -*- coding: utf-8 -*-
from argparse import ArgumentError
from django.db.models import Count
from django.core.management.base import BaseCommand, CommandError

from general.models import Document, People


class Command(BaseCommand):
    """Filtering of people by specifying their education"""

    @staticmethod
    def pair(arg):
        """Custom type for parsing education types:
        Args: str
            Example: ' primary school , secondary school ,,, '
        Returns:
            list: education types
            ['primary school', 'secondary school']
        """
        res = [x.strip() for x in unicode(arg, 'utf8').split(',') if x.strip()]
        if not res:
            raise ArgumentError()
        return res

    def get_education_ids(self):
        """Getting ids for education types

        Returns:
            list: Document ids
        """
        ids = []
        for education in self.education_list:
            try:
                obj = Document.objects.get(education__iexact=education)
            except Document.DoesNotExist:
                raise CommandError(
                    u'Education type {} does not exist'.format(education)
                )
            ids.append(obj.id)
        return ids

    def filter_people(self, ids):
        """Filtering people by document ids
        Args:
            ids (list): Document ids
        Returns:
            queryset: model People
        """
        queryset = People.objects.all()
        if self.exclude:
            queryset = queryset.exclude(documents__id__in=ids)
        else:
            queryset = queryset.filter(documents__id__in=ids).\
                annotate(num_documents=Count('documents')).\
                filter(num_documents=len(ids))

        queryset = queryset.distinct()
        return queryset

    def people_stdout(self, objects):
        """Generate stdout and write to stdout"""
        stdout = []
        template = u'({id})-{name}'

        [stdout.append(template.format(**obj.__dict__)) for obj in objects]

        stdout = u', '.join(stdout)
        self.stdout.write(stdout)

    def add_arguments(self, parser):
        parser.add_argument("education", type=self.pair,
                            help="comma separated education types")

        parser.add_argument('-exclude', action='store_true',
                            help="exclude specified education types")

    def handle(self, *args, **options):
        self.education_list = options.get('education')
        self.exclude = options.get('exclude')

        education_ids = self.get_education_ids()
        people = self.filter_people(education_ids)

        self.people_stdout(people)
