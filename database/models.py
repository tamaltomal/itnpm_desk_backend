from datetime import timedelta, datetime
import uuid
from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.
class AccessHour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=150, null=False)
    date = models.DateTimeField()

    def extend(self):
        return f'absolute end {(datetime.now() + timedelta(days=7)).strftime("%I:%M %d %B %Y")}'

    def __str__(self):
        return f'Name: {self.name}, Expire at: {self.date}'

class Pool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=False)
    address_range = models.CharField(max_length=35, null=False)

    def __str__(self):
        return f'Name: {self.name}, Range: {self.address_range}'

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    ipv4 = models.CharField(max_length=15, null=False)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name = 'addresses')

    def __str__(self):
        return f'Address: {self.ipv4}, Belongs to: {self.pool}'

class AccessList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=150, null=False)
    line = models.TextField(null=False)

    def add_line(self, new_line):
        self.line = self.line + new_line
    
    def __str__(self):
        return f'Name: {self.name}'

class Policy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=False)
    sim_login = models.IntegerField(null=True)
    access_lists = models.ManyToManyField(AccessList)
    access_hours = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'Name: {self.name}'

class Tunnel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=False)
    auth_server = models.CharField(max_length=20, null=False)
    url = models.CharField(max_length=200, null=False)
    pools = models.ManyToManyField(Pool, related_name='+')
    policies = models.ManyToManyField(Policy, related_name='+')
    updated = models.DateTimeField(auto_now_add=True)
    approval = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'Name: {self.name}'