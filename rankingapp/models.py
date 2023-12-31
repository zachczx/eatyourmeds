from django.db import models
import uuid 

# Create your models here.

class Sequence(models.Model):
    lookup_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    order = models.IntegerField(blank=False, default=100_000)

class Session(models.Model):
    user_defined = models.CharField(primary_key=True, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

class Worker(models.Model):
    name = models.CharField(null=False, blank=False)
    session = models.ForeignKey(Session, blank=False, null=False, default=None, on_delete=models.CASCADE)
    dept = models.CharField(null=True, blank=True, default=None)
    rank_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)