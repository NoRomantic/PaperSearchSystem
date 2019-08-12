from django.db import models


# Create your models here.
class PaperInfo(models.Model):
    papername = models.CharField(max_length=500, unique=False)
    journal = models.CharField(max_length=200)
    fenqu = models.IntegerField()
    top = models.BooleanField(default=False)
    impactfactor = models.FloatField()
    cites = models.IntegerField()
    esi = models.BooleanField(default=False)

    def __str__(self):
        return self.papername


class UnsearchedPapers(models.Model):
    papername = models.CharField(max_length=500, unique=True)
    journal = models.CharField(max_length=200)


class BasicInfo(models.Model):
    title = models.CharField()
    nsfc_youth = models.BooleanField()
    nsfc_face = models.BooleanField()
    nsfc_key = models.BooleanField()


class ProjectFunding(models.Model):
    project_name = models.CharField()
    funding = models.FloatField()


class Patents(models.Model):
    patent_name = models.CharField()
    domestic = models.BooleanField()
