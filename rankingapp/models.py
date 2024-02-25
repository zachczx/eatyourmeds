from django.db import models
import uuid 

# Create your models here.

class Sequence(models.Model):
    lookup_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    order = models.IntegerField(blank=False, default=100_000)
    
    def __str__(self):
        return self.lookup_id

class Session(models.Model):
    user_defined = models.CharField(primary_key=True, null=False, blank=False, max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    sequence = models.CharField(null=True, blank=True, max_length=10000)
    user_quotaB = models.IntegerField(null=True, blank=True)
    user_quotaC = models.IntegerField(null=True, blank=True)
    user_quotaD = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.user_defined

class Worker(models.Model):
    name = models.CharField(null=False, blank=False)
    session = models.ForeignKey(Session, blank=False, null=False, default=None, on_delete=models.CASCADE)
    dept = models.CharField(null=True, blank=True, default=None)
    rank_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    order = models.IntegerField(null=True, default=None)
    prev = models.CharField(null=True, blank=True, max_length=5)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name