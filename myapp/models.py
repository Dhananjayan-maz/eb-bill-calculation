from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Customer(models.Model):
    eb_service_num = models.CharField(max_length=20, null=True, blank=True, unique=True) 
    cus_name = models.CharField(max_length=100, null=True, blank=True)
    cus_address = models.TextField( null=True, blank=True)
    cus_email = models.EmailField( null=True, blank=True)
    install_date = models.DateField( null=True, blank=True)
    cus_password= models.CharField(max_length=128, unique=True, null=True, blank=True)   # Store hashed passwords
    tariff_category = models.CharField(max_length=10,  choices=[('Domestic', 'Domestic'), ('Commercial', 'Commercial'), ('Industrial', 'Industrial')])
    
    def initials(self):
        parts = self.cus_name.strip().split()
        if len(parts) > 1:
            return (parts[0][0] + parts[-1][0]).upper()
        else:
            return self.cus_name[:2].upper()
        
    def __str__(self):
        return f"{self.cus_name} ({self.eb_service_num})"
    
class TariffCategory(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Residential", "Commercial", "Industrial"
    
    
    def __str__(self):
        return self.name



class per_unit_price_model(models.Model):
    eb_service_num = models.ForeignKey(Customer, to_field='eb_service_num', on_delete=models.CASCADE, related_name='bills_by_service_num')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="per_unit_prices")
    category_name =  models.ForeignKey("TariffCategory", on_delete=models.PROTECT) # residential, commercial, industrial
    reading_date = models.DateField()
    starting_unit = models.IntegerField()
    ending_unit = models.IntegerField()
    #rate_per_unit = models.DecimalField(max_digits=10, decimal_places=2) 

def __str__(self):
    return self.category_name.name


class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    eb_service_num = models.CharField(max_length=20)
    address= models.TextField()
    TariffCategory= models.CharField(max_length=10)
    reading_date= models.DateField()
    billing_period_start = models.DateField() 
    billing_period_end = models.DateField()
    bill_date = models.DateField(default=timezone.localdate)
    previous_reading= models.IntegerField()
    current_reading= models.IntegerField() 
    units_consumed = models.IntegerField() 
    due_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) 



    def __str__(self):
        return f"Bill for {self.customer} ({self.billing_period_start} - {self.billing_period_end})"
        
    
class Payment(models.Model):
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=50, choices=[('online','Online'),('cash','Cash'),('cheque','Cheque')])
    payment_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)



class Employee(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50) 
    emp_con_num = models.CharField(max_length=15, blank=True, null=True)
    emp_email = models.EmailField(blank=True, null=True)
    emp_password= models.CharField(max_length=128, blank=True, null=True, unique=True)   # Store hashed passwords
    emp_address = models.TextField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    region = models.CharField(max_length=100, choices=[('North Region', 'North Region'), ('South Region', 'South Region'), ('East Region', 'East Region'), ('West Region', 'West Region'), ('Central Region', 'Central Region')])
   
    def initials(self):
        # strip whitespace just in case
        first = (self.first_name or '').strip()
        last  = (self.last_name  or '').strip()

        if first and last:
            # take first letter of both
            return (first[0] + last[0]).upper()
        elif first:
            # no last name, take first two letters of first name
            return first[:2].upper()
        else:
            return ''

    def __str__(self):
        return f"{self.employee_id} – {self.first_name} {self.last_name}"
    
class previewreadings(models.Model):
    Customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    reading_date=models.DateField()
    eb_service_num = models.CharField(max_length=20)
    previous_reading= models.IntegerField()
    current_reading= models.IntegerField() 
    units_consumed = models.IntegerField() 
    status=models.CharField(max_length=20, choices=[('Pending','Pending'),('Reviewed','Reviewed')], default='Pending') 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_period_start = models.DateField() 
    billing_period_end = models.DateField()

    