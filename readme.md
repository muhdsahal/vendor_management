
---

### Project Overview:

I built a system to manage vendors and their orders using Django. The goal was to create a place where vendors' details and orders could be handled easily.

### What I Did:

1. **Vendor Management:**
   - Made a way to add, see, update, and remove vendor details like names, contacts, and addresses.
  
2. **Order Tracking:**
   - Set up a system to follow orders - their numbers, what's ordered, and when they're due.
  
3. **Evaluating Vendor Performance:**
   - Added a method to see how well vendors are doing - like if they deliver on time and the quality of their work.
  
### How I Made It Happen:

- **Technology Used:** I used Django and Django REST Framework.
  
- **Key Achievements:**
   - Set up a way for only allowed people to access the system using tokens.
   - Learned about a new system (signals) to make the system work better.

- **Testing and Notes:**
   - Checked everything was working using a tool called Postman.
   - Wrote down all the steps in a document so others can understand and use it later.

### What I Learned:

I found out a lot about how to make systems work better. I also learned new ways to secure systems and how to check if they're working well.

### How I Felt:

It was tough! I worked for three days without a break, but it was worth it. I learned a lot and made something that works well.

### The End Result:

I made a system to manage vendors and orders smoothly. Even though it was tough, it turned out great and taught me a lot.

---



Installation process 



---

## Project Structure

The project is structured as follows:

- `api/` - Django project folder
- `vendors/` - Django app for vendor management
- `venv/` - Virtual environment for Python

## Setup Instructions

### 1. Create Virtual Environment

```
    py -m venv venv
```

### 2. Activate Virtual Environment

```
    venv\scripts\activate
```

### 3. Install Dependencies

Install required packages using pip:

```
    pip install django djangorestframework django-cors-headers
```

### 4. Create Django Project and App

```

    django-admin startproject backend
    django-admin startapp api
```

### 5. Configuration

#### Update `settings.py`

Add the following apps to `INSTALLED_APPS` in `api/settings.py`:

```
    INSTALLED_APPS = [
        # ...
        'vendors',
        'rest_framework',
        'corsheaders',
	'rest_authtoken',
        # ...
    ]
```

#### Configure CORS

Add the CORS middleware to `MIDDLEWARE` in `api/settings.py`:

```
    MIDDLEWARE = [
        # ...
        'corsheaders.middleware.CorsMiddleware',
        # ...
    ]
```

### 6. URL Configuration

Connect app URLs to project URLs in `api/urls.py`:

```
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
    path('vendors/', VendorList.as_view(), name='vendor-list'),  
    path('vendors/<int:vendor_id>/', VendorDetail.as_view(), name='vendor-detail'),  
    path('purchase_orders/', PurchaseOrderList.as_view(), name='purchase-orders'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderDetails.as_view(), name='purchase-details'),
    path('vendors/<int:vendor_id>/performance/', PerformenceList.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),


]
```

### 7. Database Setup

Run Django migrations to set up the database:

```
    python manage.py makemigrations
    python manage.py migrate
```

### 8. Run Development Server

Start the development server:

```
    python manage.py runserver
```


```
    pip install djangorestframework-authtoken
```

## setup in settings

```
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_authtoken.auth.AuthTokenAuthentication',
        ),
    } 

```
- Access the Django admin interface at `http://localhost:8000/admin/` to manage vendors and users.
- Utilize the endpoints defined in the `vendors` app for vendor management (e.g., `http://localhost:8000/vendors/`).

## Additional Notes

- Ensure proper permissions and authentication mechanisms are implemented for sensitive operations.
- Customize and extend the functionalities as needed for your specific use case.

---

