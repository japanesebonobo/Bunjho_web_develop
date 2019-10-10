from django.db import models

# Create your models here.
class Bunjho_web_database(models.Model):
    subjectData_index = models.IntegerField()
    subjectNo = models.TextField()
    faculty = models.TextField()
    subjectName = models.TextField()
    teacher = models.TextField()
    place = models.TextField()
    units = models.TextField()
    scoreData_index = models.IntegerField()
    member = models.IntegerField()
    A = models.FloatField()
    B = models.FloatField()
    C = models.FloatField()
    D = models.FloatField()
    F = models.FloatField()
    other = models.IntegerField()
    averageGPA = models.FloatField()
    linkData_index = models.IntegerField()
    link = models.TextField()

class Allsubjectdata(models.Model):
    subjectno = models.IntegerField(db_column='subjectNo', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    faculty = models.TextField(blank=True, null=True)
    subjectname = models.TextField(db_column='subjectName', blank=True, null=True)  # Field name made lowercase.
    teacher = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    units = models.TextField(blank=True, null=True)
    member = models.IntegerField(blank=True, null=True)
    a = models.FloatField(db_column='A', blank=True, null=True)  # Field name made lowercase.
    b = models.FloatField(db_column='B', blank=True, null=True)  # Field name made lowercase.
    c = models.FloatField(db_column='C', blank=True, null=True)  # Field name made lowercase.
    d = models.FloatField(db_column='D', blank=True, null=True)  # Field name made lowercase.
    f = models.FloatField(db_column='F', blank=True, null=True)  # Field name made lowercase.
    other = models.IntegerField(blank=True, null=True)
    averagegpa = models.FloatField(db_column='averageGPA', blank=True, null=True)  # Field name made lowercase.
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AllSubjectData'

    def __str__(self):
        return self.subjectno
