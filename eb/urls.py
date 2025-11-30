# """
# URL configuration for eb project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path

# from myapp import views

# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('index/', views.index, name='index'),
#     path('bill/<int:customer_id>/<int:bill_id>/', views.generate_bill, name='bill'),
#     path('customer/', views.customer_dashboard, name='customer_dashboard'),
#     path('customer_login/', views.customer_login, name='customer_login'),
#     path('customer_signup/', views.customer_signup, name='customer_signup'),
#     path('employee/', views.employee, name='employee_dashboard'),
#     path('employee_login/', views.employee_login, name='employee_login'),
#     path('employee_signup/', views.employee_signup, name='employee_signup'),
#     path('meter/', views.meter_reading, name='meter_reading'),
#     path('logout/', views.user_logout, name='user_logout'),
#     path('emp_bill/', views.emp_bill, name='emp_bill'),
# ]

from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('bill/<int:customer_id>/', views.preview_bill, name='bill'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('employee/', views.employee, name='employee_dashboard'),
    path('employee_login/', views.employee_login, name='employee_login'),
    path('employee_signup/', views.employee_signup, name='employee_signup'),
    path('meter/', views.meter_reading, name='meter_reading'),
    path('logout/', views.user_logout, name='logout'),
    path('emp_bill/<int:pre_bill_id>/', views.emp_bill, name='emp_bill'),  # detail
    path('emp_bills/', views.emp_bills_list, name='emp_bills'),         # list of previews
]   