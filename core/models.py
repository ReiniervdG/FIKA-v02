import hashlib

from django.db import models

BASE_URL = 'https://www.fika.com/'


class Provider(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=50)
    limit = models.IntegerField()

    def __str__(self):
        return self.name


class FikaID(models.Model):
    fika_code = models.CharField(max_length=100, editable=False)
    qr_string = models.CharField(max_length=100, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField()

    def save(self, *args, **kwargs):
        hash_code = hashlib.sha256(str(self.id).encode('utf-8')).hexdigest()
        self.fika_code = hash_code
        self.qr_string = BASE_URL + 'redeem/' + hash_code
        super(FikaID, self).save(*args, **kwargs)

    def __str__(self):
        return f'FikaID {self.id}'


class Transaction(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fika_id = models.ForeignKey(FikaID, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'FikaID {self.fika_id.id} at {self.provider.name}'

