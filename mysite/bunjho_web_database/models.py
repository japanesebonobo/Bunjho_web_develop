from django.db import models

class Allsubjectdata(models.Model):
    subjectno = models.TextField(db_column='subjectNo', blank=True, null=False, primary_key=True) 
    faculty = models.TextField(blank=True, null=True)
    subjectname = models.TextField(db_column='subjectName', blank=True, null=True) 
    teacher = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    units = models.TextField(blank=True, null=True)
    member = models.IntegerField(blank=True, null=True)
    a = models.FloatField(db_column='A', blank=True, null=True)  
    b = models.FloatField(db_column='B', blank=True, null=True)  
    c = models.FloatField(db_column='C', blank=True, null=True)  
    d = models.FloatField(db_column='D', blank=True, null=True)  
    f = models.FloatField(db_column='F', blank=True, null=True)  
    # other = models.IntegerField(blank=True, null=True) 
    averagegpa = models.FloatField(db_column='averageGPA', blank=True, null=True) 
    link = models.TextField(db_column='link', blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'AllSubjectData'

    def __str__(self):
        return self.subjectno

GENERATION_CHOICES = [
    ('', '選択肢から選んでください'),
    ('学部', '学部生'),
    ('博前', '大学院生'),
]

GENRE_CHOICES = {
    ('', '選択肢から選んでください'),
    ('h', '必修科目'),
    ('a', 'A群'),
    ('b', 'B群'),
    ('c', 'C群'),
    ('o', 'その他')
}

class User(models.Model):
    faculty = models.TextField('課程', max_length=1, choices=GENERATION_CHOICES)
    subjectno = models.TextField('科目ジャンル', max_length=1, choices=GENRE_CHOICES)
    subjectname = models.CharField('名前', max_length=100)
    teacher = models.CharField('教員名', max_length=100)