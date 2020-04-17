# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Entries(models.Model):
    sub_project_index = models.ForeignKey('SubProjects', models.DO_NOTHING, db_column='sub_project_index', blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    start_at = models.TimeField(blank=True, null=True)
    end_at = models.TimeField(blank=True, null=True)
    span = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entries'


class Projects(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class SubProjects(models.Model):
    index = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, models.DO_NOTHING, blank=True, null=True)
    activity_number = models.CharField(max_length=2)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sub_projects'
