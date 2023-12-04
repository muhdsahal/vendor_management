from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.ModelSerializer): # vendor serializer find all
    class Meta:
        model = vendor
        fields = "__all__"

class PurchaseOrderSerializer(serializers.ModelSerializer): #purchase order serializer find all
    class Meta:
        model = purchase_order
        fields = "__all__"
        
class HistoricalPerformenceSerializer(serializers.ModelSerializer): 
    #historical performence serialzer find specifc data
    class Meta:
        model = historical_performence
        fields = ['vendor','date','on_time_delivery_rate', 'quality_rating_avg', 
                  'average_response_time', 'fulfillment_rate']
