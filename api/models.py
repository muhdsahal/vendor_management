from datetime import timedelta
from django.db import models
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from django.db.models import F,Avg
from rest_framework.authtoken.models import Token as DRFToken
# Create your models here.
class vendor(models.Model):
    name = models.CharField(max_length=100,blank=False)

    contact_details = models.TextField()

    address = models.TextField()

    vendor_code = models.CharField(max_length=4, unique=True)

    on_time_delivery_rate = models.FloatField()

    quality_rating_avg = models.FloatField()

    average_response_time = models.FloatField()

    fulfillment_rate = models.FloatField()

    
class purchase_order(models.Model):
    STATUS_CHOICES=[
        ('pending','pending'),
        ('completed','completed'),
        ('canceled','canceled')
    ]

    po_number = models.CharField(max_length=4,unique=True)

    vendor = models.ForeignKey(vendor,on_delete=models.CASCADE)

    order_date = models.DateTimeField()

    delivery_date = models.DateTimeField()

    items = models.JSONField()

    quantity = models.IntegerField()

    status = models.CharField(max_length=20,choices=STATUS_CHOICES)

    quality_rating = models.FloatField(null=True,blank=True)

    issue_date = models.DateTimeField()

    acknowledgment_date = models.DateTimeField(null=True, blank=True)

class historical_performence(models.Model):

    vendor = models.ForeignKey(vendor,on_delete=models.CASCADE)

    date = models.DateTimeField()

    on_time_delivery_rate = models.FloatField(default=00)

    quality_rating_avg = models.FloatField(default=00)

    average_response_time = models.FloatField(default=00)

    fulfillment_rate = models.FloatField(default=00)

class vendor_token(models.Model):
    key = models.CharField(max_length=40,unique=True)

    vendor = models.OneToOneField(vendor,related_name='auth_token',on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

# Separate functions for performance metric calculations
def calculate_on_time_delivery_rate(vendor):
    # Calculation  for on-time delivery rate
    completed_orders = purchase_order.objects.filter(
        vendor=vendor, status='completed'
    ).count()

    on_time_delivery_orders = purchase_order.objects.filter(
        vendor=vendor, status='completed', delivery_date__lte=F('acknowledgment_date')
    ).count()

    return on_time_delivery_orders / completed_orders if completed_orders else 0

def calculate_quality_rating_avg(vendor):
    # Calculation  quality rating average
    return purchase_order.objects.filter(
        vendor=vendor, status='completed', quality_rating__isnull=False
    ).aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

def calculate_average_response_time(vendor):
    # Calculation  average response time
    response_times = purchase_order.objects.filter(
        vendor=vendor, acknowledgment_date__isnull=False
    ).annotate(response_time=F('acknowledgment_date') - F('issue_date')).aggregate(
        avg_time=Avg('response_time')
    )['avg_time'] or timedelta(0)

    return response_times.total_seconds() / 60

def calculate_fulfillment_rate(vendor):
    # Calculation  fulfillment rate
    total_orders = purchase_order.objects.filter(vendor=vendor).count()
    fulfilled_orders = purchase_order.objects.filter(
        vendor=vendor, status='completed', quality_rating__isnull=False
    ).count()

    return fulfilled_orders / total_orders if total_orders else 0

# Signal  function
@receiver(post_save, sender=purchase_order)
def update_vendor_performance(sender, instance, created, **kwargs):
    if not created:
        vendor = instance.vendor

        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = calculate_quality_rating_avg(vendor)
        average_response_time = calculate_average_response_time(vendor)
        fulfillment_rate = calculate_fulfillment_rate(vendor)

        # update / create historical performence record data
        with transaction.atomic():
            historical_record, created = historical_performence.objects.get_or_create(
                vendor=vendor, date=timezone.now(),
                defaults={
                    'on_time_delivery_rate': on_time_delivery_rate,
                    'quality_rating_avg': quality_rating_avg,
                    'average_response_time': average_response_time,
                    'fulfillment_rate': fulfillment_rate
                }
            )

            if not created:
                # update existing historical record
                historical_record.on_time_delivery_rate = on_time_delivery_rate
                historical_record.quality_rating_avg = quality_rating_avg
                historical_record.average_response_time = average_response_time
                historical_record.fulfillment_rate = fulfillment_rate
                historical_record.save()

#create token for secure authentication
@receiver(post_save,sender=vendor)
def create_vendor_token(sender,instance,created, **kwargs):
    if created:
        token = DRFToken.objects.create(vendor=instance)
        vendor_token.objects.create(vendor=instance,key=token.key)