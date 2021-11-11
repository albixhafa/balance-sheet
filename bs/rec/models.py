from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
import uuid
import os

# Create your models here.

class Entity(models.Model):
    entity = models.CharField(max_length=40)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.entity

class Period(models.Model):
    period = models.CharField(max_length=7, validators=[MinLengthValidator(7)])

    def __str__(self):
        return self.period

class Status(models.Model):
    option = models.CharField(max_length=40)

    def __str__(self):
        return self.option

class Gldetail(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, default=None, blank=True, null=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, default=None, blank=True, null=True)
    glnum = models.CharField(max_length=12, validators=[MinLengthValidator(12)], verbose_name='GL Number')
    gldesc = models.CharField(max_length=40, verbose_name='GL Description')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usernames', editable=False)
    glamt = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='GL Amount')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('gldetail-update', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.entity} - {self.period} - {self.glnum}"

    class Meta:
        unique_together = (('entity','period','glnum'),)

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('documents/', filename)

class Glpost(models.Model):
    gldetail = models.ForeignKey(Gldetail, on_delete=models.CASCADE, default=None, blank=True, null=True)
    jdate = models.CharField(max_length=10, validators=[MinLengthValidator(10)], verbose_name='Date')
    jref = models.CharField(max_length=6, validators=[MinLengthValidator(6)], verbose_name='Reference')
    jamt = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='Amount')
    jdesc = models.CharField(max_length=20, verbose_name='Description')
    jattach = models.FileField(upload_to=get_file_path, verbose_name='Support Attachment', default=None, blank=True, null=True)

    def __str__(self):
        return self.jref