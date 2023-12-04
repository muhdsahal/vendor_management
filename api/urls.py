from django.urls import path
from .views import (
    VendorDetail, VendorList,
    PurchaseOrderDetails, PurchaseOrderList, PerformenceList
    ,AcknowledgePurchaseOrderView
)

urlpatterns = [
    path('vendors/', VendorList.as_view(), name='vendor-list'),  
    # list all vendors and create a new vendor
    path('vendors/<int:vendor_id>/', VendorDetail.as_view(), name='vendor-detail'),  
    # retrieve, update, delete a specific vendor
    path('purchase_orders/', PurchaseOrderList.as_view(), name='purchase-orders'),
    # list all purchase_order and create a new purchase_order
    path('purchase_orders/<int:po_id>/', PurchaseOrderDetails.as_view(), name='purchase-details'),
    # retrieve, update, delete a specific purchase order
    path('vendors/<int:vendor_id>/performance/', PerformenceList.as_view(), name='vendor-performance'),
    # retrieve performance metrics for a specific vendor
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
    # create vendors to acknowledge po


]
