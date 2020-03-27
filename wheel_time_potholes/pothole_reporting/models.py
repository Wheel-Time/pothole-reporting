# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# Generated using 'python manage.py inspectdb --include-views > models.py'
# TODO: Properly configure all models. Maybe make a trello card?
class Pothole(models.Model):
    lat = models.DecimalField(max_digits=11, decimal_places=8)
    lon = models.DecimalField(max_digits=11, decimal_places=8)
    create_date = models.DateTimeField()

    class Meta:
        managed = False     # All pre-existing tables, so false should be kept UNLESS we want to generate from django
        db_table = 'pothole'


class PotholeLedger(models.Model):
    fk_pothole = models.ForeignKey(Pothole, models.DO_NOTHING)
    fk_user = models.ForeignKey('SiteUser', models.DO_NOTHING)
    state = models.IntegerField()
    submit_date = models.DateTimeField()

    class Meta:
        managed = False     # All pre-existing tables, so false should be kept UNLESS we want to generate from django
        db_table = 'pothole_ledger'


class SiteUser(models.Model):
    username = models.CharField(unique=True, max_length=32)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    pword = models.CharField(max_length=128)
    is_admin = models.IntegerField()

    class Meta:
        managed = False     # All pre-existing tables, so false should be kept UNLESS we want to generate from django
        db_table = 'site_user'


class VwPothole(models.Model):
    id = models.IntegerField(primary_key=True)
    lat = models.DecimalField(max_digits=11, decimal_places=8)
    lon = models.DecimalField(max_digits=11, decimal_places=8)
    create_date = models.DateTimeField()
    effective_date = models.CharField(max_length=76, blank=True, null=True)
    fixed_date = models.CharField(max_length=76, blank=True, null=True)
    pothole_reports = models.DecimalField(max_digits=23, decimal_places=0, blank=True, null=True)
    fixed_reports = models.DecimalField(max_digits=23, decimal_places=0, blank=True, null=True)

    def save(self):
        return  # disallow saving to view

    def delete(self):
        return  # disallow deleting from view

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_pothole'
