from django.db import models
from django.urls import reverse


# Create your models here.

class Device(models.Model):
    sapid = models.CharField(max_length=18,blank=True,null=True)
    hostname = models.CharField(max_length=14,blank=True,null=True)
    loopback = models.CharField(max_length=16,blank=True,null=True)
    mac_address = models.CharField(max_length=17,blank=True,null=True)
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")
    ip_address = models.CharField(max_length=17,blank=True,null=True)

    def __str__(self):
        return self.hostname

    def get_absolute_url(self):
        return reverse('book_edit', kwargs={'pk': self.pk})

