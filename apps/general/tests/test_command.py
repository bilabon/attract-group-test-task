# -*- coding: utf-8 -*-
from StringIO import StringIO
from django.test import TestCase

from django.core.management import call_command
from django.core.management.base import CommandError

from general.tests.base import DocumentFactory, PeopleFactory
from general.models import Document, People


class FilterPeople(TestCase):
    """Base configs for tests"""

    def setUp(self):
        Document.objects.all().delete()
        doc_1 = DocumentFactory(id=1, education='Preschool')
        doc_2 = DocumentFactory(id=2, education='Primary school')
        doc_3 = DocumentFactory(id=3, education=u'Лицей')

        People.objects.all().delete()
        PeopleFactory.create(id=1, name='Alf', documents=(doc_1, doc_2))
        PeopleFactory.create(id=2, name='Anton', documents=(doc_1, ))
        PeopleFactory.create(id=3, name=u'Кирил', documents=(doc_2, ))
        PeopleFactory.create(id=4, name='John', documents=(doc_3, ))

    def test_initial(self):
        self.assertEqual(Document.objects.count(), 3)
        self.assertEqual(People.objects.get(id=1).documents.count(), 2)

    def test_command_filter_people_stdout(self):
        """Testing stdout of command."""
        # checking 1
        stdout = StringIO()
        call_command('find_people', 'Preschool, Primary school', stdout=stdout)
        self.assertEqual(u'(1)-Alf\n', stdout.getvalue())

        # checking 2
        stdout = StringIO()
        call_command('find_people', '-exclude', 'Preschool, Primary school', stdout=stdout)
        self.assertEqual(u'(4)-John\n', stdout.getvalue())

        # checking 3
        stdout = StringIO()
        call_command('find_people', ' ,primary school,,,', stdout=stdout)
        self.assertEqual(u'(1)-Alf, (3)-Кирил\n', unicode(stdout.getvalue(), 'utf8'))

    def test_command_filter_people_exeption(self):
        """Checking for CommandError"""

        # check for an invalid args
        self.assertRaises(CommandError, call_command, 'find_people', '!,')

        # check if not exist
        self.assertRaises(CommandError, call_command, 'find_people', 'Pres5chool')
