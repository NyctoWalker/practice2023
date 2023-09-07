# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse
import os.path
from os import path


class Exhibit(models.Model):
    exhibit_id = models.AutoField(primary_key=True)
    exhibit_name = models.CharField(unique=True, max_length=45)
    exhibit_desc = models.CharField(max_length=1000, blank=True, null=True)
    exhibit_author = models.CharField(max_length=45, blank=True, null=True)
    setting_date = models.DateField(blank=True, null=True)
    id_status = models.ForeignKey('Statuses', models.DO_NOTHING, db_column='id_status')
    exhibit_picture = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'exhibit'
        unique_together = (['exhibit_id', 'id_status'])
        verbose_name_plural = 'Экспонаты'

    def __str__(self):
        return f"{self.exhibit_name} ({self.exhibit_id})"

    def get_expositions(self):
        expexhibit = ExpositionExhibits.objects.filter(id_exhibit_exposition=self.exhibit_id)
        expo = Exposition.objects.filter(exposition_id__in=expexhibit.values('id_exposition'))
        return expo

    def exhibit_get_picture(self):
        if os.path.isfile(os.path.join(os.path.dirname(__name__), f"main_page/static/main_page/pic/objects/{self.exhibit_picture}")):
            pic_path = f"main_page/pic/objects/{self.exhibit_picture}"
        else:
            pic_path = f"main_page/pic/notdef-solid.svg"
        return pic_path


class ExhibitTags(models.Model):
    id_tag = models.ForeignKey('Tags', models.DO_NOTHING, db_column='id_tag')  # The composite primary key (id_tag, id_exhibit_tag) found, that is not supported. The first column is selected.
    id_exhibit_tag = models.ForeignKey(Exhibit, models.DO_NOTHING, db_column='id_exhibit_tag')

    class Meta:
        db_table = 'exhibit_tags'
        unique_together = (('id_tag', 'id_exhibit_tag'),)
        verbose_name_plural = 'Теги экспонатов'

    def __str__(self):
        return f"{self.id_exhibit_tag} ({self.id_tag})"


class Exposition(models.Model):
    exposition_id = models.AutoField(primary_key=True)  # The composite primary key (exposition_id, id_hall) found, that is not supported. The first column is selected.
    exposition_name = models.CharField(unique=True, max_length=45)
    exposition_desc = models.CharField(max_length=1000, blank=True, null=True)
    id_hall = models.ForeignKey('Hall', models.DO_NOTHING, db_column='id_hall')
    exposition_picture = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'exposition'
        unique_together = (('exposition_id', 'id_hall'),)
        verbose_name_plural = 'Экспозиции'

    def __str__(self):
        return f"{self.exposition_name} ({self.exposition_id})"
    
    def get_exhibits(self):
        expexpon = ExpositionExhibits.objects.filter(id_exposition=self.exposition_id)
        exhib = Exhibit.objects.filter(exhibit_id__in=expexpon.values('id_exhibit_exposition'))
        return exhib

    def exposition_get_picture(self):
        if os.path.isfile(os.path.join(os.path.dirname(__name__), f"main_page/static/main_page/pic/objects/{self.exposition_picture}")):
            pic_path = f"main_page/pic/objects/{self.exposition_picture}"
        else:
            pic_path = f"main_page/pic/notdef-solid.svg"
        return pic_path


class ExpositionExhibits(models.Model):
    id_exposition = models.ForeignKey(Exposition, models.DO_NOTHING, db_column='id_exposition')  # The composite primary key (id_exposition, id_exhibit_exposition) found, that is not supported. The first column is selected.
    id_exhibit_exposition = models.OneToOneField(Exhibit, models.DO_NOTHING, db_column='id_exhibit_exposition')
    # id_exhibit_exposition = models.ForeignKey(Exhibit, models.DO_NOTHING, db_column='id_exhibit_exposition', unique=True)

    class Meta:
        db_table = 'exposition_exhibits'
        unique_together = (('id_exposition', 'id_exhibit_exposition'),)
        verbose_name_plural = 'Экспонаты экспозиций'

    def __str__(self):
        return f"{self.id_exposition} ({self.id_exhibit_exposition})"


class Hall(models.Model):
    FLOORS = (
        (1, "1 этаж"),
        (2, "2 этаж"),
        (3, "3 этаж"),
        (4, "Зал заморожен")
    )

    hall_id = models.AutoField(primary_key=True)
    hall_name = models.CharField(unique=True, max_length=45)
    hall_desc = models.CharField(max_length=1000, blank=True, null=True)
    floor_number = models.IntegerField(choices=FLOORS, blank=False)

    class Meta:
        db_table = 'hall'
        verbose_name_plural = 'Залы музея'

    def __str__(self):
        if self.floor_number != 4:
            name_hall = f"Зал {self.hall_name}, {self.floor_number} этаж ({self.hall_id})"
        else:
            name_hall = f"Зал {self.hall_name}, заморожен ({self.hall_id})"
        return name_hall

    def hall_get_exposition(self):
        expos = Exposition.objects.filter(id_hall=self.hall_id)
        return expos


class Statuses(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(unique=True, max_length=45)

    class Meta:
        db_table = 'statuses'
        verbose_name_plural = 'Перечень статусов'

    def __str__(self):
        return f"{self.status_name} ({self.status_id})"


class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'tags'
        verbose_name_plural = 'Перечень тегов'

    def __str__(self):
        return f"{self.tag_name} ({self.tag_id})"


class Tickets(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_date = models.DateTimeField(blank=False, null=True)
    phone_number = models.CharField(max_length=12, null=True)

    class Meta:
        db_table = 'tickets'
        verbose_name_plural = 'Билеты'

    def __str__(self):
        return f"{self.ticket_id} - {self.ticket_date} (+{self.phone_number})"