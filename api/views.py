from datetime import datetime
from django.http import Http404
from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
# Create your views here.


class VendorList(APIView):

    #token authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request): #retrive all the data
        vendors = vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request): # add data to vendor
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class VendorDetail(APIView):
    #token authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, vendor_id): #get specific data create function
        try:
            return vendor.objects.get(id=vendor_id)
        except vendor.DoesNotExist:
            raise Http404

    def get(self, request, vendor_id): #get specific data using id
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, vendor_id): # update specific data
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id): #delete specific data
        vendor = self.get_object(vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PurchaseOrderList(APIView): # purchase order list,create

    #token authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request): # retrive all the data
        queryset = purchase_order.objects.all()
        serializer = PurchaseOrderSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def post(self,request): #add submit data
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetails(APIView):# purshase order using specific

    #token authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self,po_id): # create function  find specific data
        try:
            return purchase_order.objects.get(id=po_id)
        except purchase_order.DoesNotExist:
            raise Http404

    def get(self,request,po_id): # get specific data
        purchase_order = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)
    
    def put(self,request,po_id): # update specific data
        purchase_order = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(purchase_order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,po_id): # delete a specifc data
        purchase_order = self.get_object(po_id)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PerformenceList(APIView): # historical performence list
    #token authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_id): #get specifc data
        his_per = historical_performence.objects.filter(vendor_id=vendor_id)
        serializer = HistoricalPerformenceSerializer(his_per, many=True)

        performance_metrics = []
        for record in serializer.data:# append all data to an array
            performance = {
                'on_time_delivery_rate': record['on_time_delivery_rate'],
                'quality_rating_avg': record['quality_rating_avg'],
                'average_response_time': record['average_response_time'],
                'fulfillment_rate': record['fulfillment_rate']
            }
            performance_metrics.append(performance)
        
        return Response(performance_metrics)

    
    def post(self, request, vendor_id): #add/submit to data
        serializer = HistoricalPerformenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor_id=vendor_id)  # Assign the vendor ID to the record
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AcknowledgePurchaseOrderView(APIView): # acknowledgment data
    #token authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):  #add/ submit data
        try:
            purchase_order_ = purchase_order.objects.get(pk=pk)
        except purchase_order.DoesNotExist:
            return Response({"error":"purchase order not found"},status=status.HTTP_404_NOT_FOUND)
        
        if purchase_order_.acknowledgment_date:
            return Response({'error': 'Purchase Order already acknowledged'}, status=status.HTTP_400_BAD_REQUEST)
        
        purchase_order_.acknowledgment_date = datetime.now()
        purchase_order_.save()

        return Response({'message': 'Purchase Order acknowledged successfully'}, status=status.HTTP_200_OK)
