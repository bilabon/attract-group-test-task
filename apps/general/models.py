# -*- coding: utf-8 -*-
from django.db import models


class Document(models.Model):
    education = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.education


class People(models.Model):
    name = models.CharField(max_length=255)
    documents = models.ManyToManyField(Document)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'people'

    def __unicode__(self):
        return self.name
