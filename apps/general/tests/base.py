# -*- coding: utf-8 -*-
import factory

from general.models import Document, People


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document


class PeopleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = People

    @factory.post_generation
    def documents(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for document in extracted:
                self.documents.add(document)
