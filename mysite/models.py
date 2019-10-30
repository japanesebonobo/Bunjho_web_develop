# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Allsubjectdata(models.Model):
    subjectdata_index = models.IntegerField(db_column='subjectData_index', blank=True, null=True)  # Field name made lowercase.
    subjectno = models.TextField(db_column='subjectNo', blank=True, null=True)  # Field name made lowercase.
    faculty = models.TextField(blank=True, null=True)
    subjectname = models.TextField(db_column='subjectName', blank=True, null=True)  # Field name made lowercase.
    teacher = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    units = models.TextField(blank=True, null=True)
    scoredata_index = models.IntegerField(db_column='scoreData_index', blank=True, null=True)  # Field name made lowercase.
    member = models.IntegerField(blank=True, null=True)
    a = models.FloatField(db_column='A', blank=True, null=True)  # Field name made lowercase.
    b = models.FloatField(db_column='B', blank=True, null=True)  # Field name made lowercase.
    c = models.FloatField(db_column='C', blank=True, null=True)  # Field name made lowercase.
    d = models.FloatField(db_column='D', blank=True, null=True)  # Field name made lowercase.
    f = models.FloatField(db_column='F', blank=True, null=True)  # Field name made lowercase.
    other = models.IntegerField(blank=True, null=True)
    averagegpa = models.FloatField(db_column='averageGPA', blank=True, null=True)  # Field name made lowercase.
    linkdata_index = models.IntegerField(db_column='linkData_index', blank=True, null=True)  # Field name made lowercase.
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AllSubjectData'
