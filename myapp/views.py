from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from.models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .decorators import *
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse 
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from .utils import compute_billing_period_for_date
from django.conf import settings


def index(request):
    return render(request, 'index.html')

@customer_session_required 
def customer_dashboard(request):   
    # user_id=request.session.get('customer_id') 
    # user = Customer.objects.get(id=user_id)
    #print(user_id) 
    customer = request.customer
    return render(request, 'customer_dashboard.html', {'customer': customer})

def customer_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')   # or 'cus_name' depending on your form
        pwd_input = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next') or reverse('customer_dashboard')

        try:
            cust = Customer.objects.get(cus_name=username)
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('customer_login')

        # If you implemented Customer.check_password(raw) use it; otherwise use check_password
        # valid = cust.check_password(pwd_input)
        valid = False
        if hasattr(cust, 'check_password'):
            valid = cust.check_password(pwd_input)
        else:
            valid = check_password(pwd_input, cust.cus_password)

        if valid:
            # rotate session key for safety
            try:
                request.session.cycle_key()
            except Exception:
                pass

            request.session['customer_id'] = cust.id

            # Validate next_url
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                next_url = reverse('customer_dashboard')

            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('customer_login')

    # GET: render form, preserve next param if present
    next_param = request.GET.get('next', '')
    return render(request, "customer_login.html", {"next": next_param})

def customer_signup(request):
    if request.method=='POST':
        eb_service_num=request.POST.get('eb_number')
        username=request.POST.get('username')
        address=request.POST.get('address')
        email=request.POST.get('email')
        install_date=request.POST.get('installed_date')
        tariff_cat=request.POST.get('tariff_category')
        password=request.POST.get('password') 
        hashed_password = make_password(password)
        confirmPassword=request.POST.get('confirm_password')
        
        if not Customer.objects.filter(cus_name=username).exists():
            if password == confirmPassword:
                customer=Customer.objects.create(
                    eb_service_num=eb_service_num,
                    cus_name=username,
                    cus_address=address,
                    cus_email=email,
                    install_date=install_date,
                    tariff_category=tariff_cat, 
                    cus_password=hashed_password,
                    )
                #print(eb_service_num,username,address,contact_number,email,install_date,password) 
                customer.save()
                messages.success(request,'Your account has been successfully created.')
                return redirect('customer_login')
        
            else:
                messages.warning(request,'your password and retype password are not match')
                return redirect('customer_signup')        
        else:
            messages.success(request,'The User was already exist')
            return render(request,'customer_signup.html')
    return render(request, 'customer_signup.html')

@employee_session_required
def employee(request):
    employee = request.employee
    employee = Employee.objects.get(id=employee.id)
    return render(request, 'employee_dashboard.html', {'employee': employee}) 

def employee_login(request): 
    if request.method == 'POST':
        empid = request.POST.get('employeeId')
        pwd_input = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next') or reverse('employee_dashboard')

        try:
            emp = Employee.objects.get(employee_id=empid)
        except Employee.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('employee_login')

        if check_password(pwd_input, emp.emp_password):
            # rotate session key for safety
            try:
                request.session.cycle_key()
            except Exception:
                # older Django or backend may not support; ignore
                pass

            request.session['employee_id'] = emp.id

            # validate next_url to avoid open redirects
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                next_url = reverse('employee_dashboard')

            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('employee_login')

    # GET: show login form. Keep next param if present
    next_param = request.GET.get('next', '')
    return render(request, "employee_login.html", {"next": next_param})    


def employee_signup(request): 
    if request.method=='POST':
        employee_id=request.POST.get('employee_id')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        emp_con_num=request.POST.get('contact_number')
        emp_email=request.POST.get('email') 
        emp_address=request.POST.get('address')
        region=request.POST.get('region')
        password=request.POST.get('password')
        hased_password = make_password(password)
        confirmpassword=request.POST.get('confirm_password')
        
        if not Employee.objects.filter(employee_id=employee_id).exists():
            if password == confirmpassword:
                employee=Employee.objects.create(
                    employee_id=employee_id,
                    first_name=first_name,
                    last_name=last_name,
                    emp_con_num=emp_con_num,
                    emp_email=emp_email,
                    emp_address=emp_address,
                    region=region,
                    emp_password=hased_password,
                )
                print(employee_id,first_name,last_name,emp_con_num,emp_email,emp_address,region,password,confirmpassword)
                employee.save()
                messages.success(request,'Your account has been successfully created.')
                return redirect('employee_login')
            
            else:
                messages.warning(request,'your password and retype password are not match')
                return redirect('employee_signup')
                
    
        else:
            messages.success(request,'The Employee ID was already exist')
            return render(request,'employee_signup.html')

        
    return render(request, 'employee_signup.html')
    
@employee_session_required
def meter_reading(request):
    employee = request.employee
    employee = Employee.objects.get(id=employee.id)

    if request.method == 'POST':
        eb_service_num = request.POST.get('eb_service_number')
        cus_name = request.POST.get('customer')            
        reading_date = request.POST.get('billing_date')
        TariffCategory = request.POST.get('tariff_category')
        starting_unit = request.POST.get('starting_unit')
        ending_unit = request.POST.get('ending_unit')
        print(eb_service_num, cus_name, reading_date, TariffCategory, starting_unit, ending_unit) 
        
        reading_date = datetime.strptime(reading_date, "%Y-%m-%d").date()
        due_date = reading_date + timedelta(days=15)
        
        try:
            starting_unit = int(starting_unit)
            ending_unit = int(ending_unit)
        except (TypeError, ValueError):
            messages.error(request, 'Starting and ending unit must be integers.')
            return redirect('meter_reading')

        # Find the actual Customer object
        try:
            customer = Customer.objects.get(eb_service_num=eb_service_num, tariff_category=TariffCategory)
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid EB Service Number or Tariff Category') 
            return redirect('meter_reading') 

        total_unit = ending_unit - starting_unit
        if total_unit < 0:
            messages.error(request, 'Ending unit must be greater than starting unit.')
            return redirect('meter_reading')

        rate_per_unit = Decimal("0.00")
        if TariffCategory == 'domestic':
            if total_unit <= 100:
                rate_per_unit = Decimal("0.00")
            elif total_unit <= 200:
                rate_per_unit = Decimal("5.00")
            elif total_unit <= 400:
                rate_per_unit = Decimal("10.00")
            elif total_unit < 1000:
                rate_per_unit = Decimal("20.00")
            else:
                rate_per_unit = Decimal("30.00")
        elif TariffCategory == 'commercial':
            if total_unit <= 100:
                rate_per_unit = Decimal("10.00")
            elif total_unit <= 200:
                rate_per_unit = Decimal("15.00")
            elif total_unit <= 400:
                rate_per_unit = Decimal("20.00")
            elif total_unit < 1000:
                rate_per_unit = Decimal("25.00")
            else:
                rate_per_unit = Decimal("30.00")
        elif TariffCategory == 'industrial':
            if total_unit <= 100:
                rate_per_unit = Decimal("10.00")
            elif total_unit <= 200:
                rate_per_unit = Decimal("20.00")
            elif total_unit <= 400:
                rate_per_unit = Decimal("30.00")
            elif total_unit < 1000:
                rate_per_unit = Decimal("40.00")
            else:
                rate_per_unit = Decimal("50.00")
        else:
            rate_per_unit = Decimal("0.00")

        total_amount = (Decimal(total_unit) * rate_per_unit).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        period_start, period_end = compute_billing_period_for_date(reading_date, cycle_day=15)
        
        # Create Bill — link to the Customer instance
        bill = Bill.objects.create(
            customer=customer,
            eb_service_num=customer.eb_service_num,
            address=customer.cus_address,
            TariffCategory=customer.tariff_category,
            billing_period_start=period_start,
            billing_period_end=period_end,
            previous_reading=starting_unit,
            current_reading=ending_unit,
            units_consumed=total_unit,
            total_amount=total_amount,
            reading_date=reading_date,
            due_date=due_date,
            # recorded_by=employee
        )
        bill.save()
        
        # Create preview reading for employee dashboard WITH ALL REQUIRED FIELDS
        pre_bill = previewreadings.objects.create(
            Customer=customer,
            reading_date=reading_date,
            eb_service_num=customer.eb_service_num,
            previous_reading=starting_unit,
            current_reading=ending_unit,
            units_consumed=total_unit,
            total_amount=total_amount,  # Add total_amount
            billing_period_start=period_start,  # Add billing period start
            billing_period_end=period_end,      # Add billing period end
            #Add any other fields your template expects
        )
        
        # Get historical bills for the same customer (excluding current one)
        history_bills = previewreadings.objects.filter(
            Customer=customer
        ).exclude(id=pre_bill.id).order_by('-reading_date')[:10]
                
        # Render the template with ALL required context data
        return render(request, 'emp_bill_review.html', {
            'pre_bill': pre_bill,
            'history_bills': history_bills,
            'employee': employee  # Add employee to context if needed in template
        })
    
    # GET request - show the meter reading form
    return render(request, 'meter_reading.html', {'employee': employee})


def preview_bill(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # find the bill (latest by reading_date)
    bill = Bill.objects.filter(customer=customer).order_by('-reading_date').first()
    print(bill)

    # Safely get employee if middleware populated it; otherwise None
    employee = getattr(request, 'employee', None)

    if not bill:
        messages.info(request, "No bills found for this customer.")
        context = {'employee': employee, 'bill': None, 'customer': customer}
        return render(request, 'bill_preview.html', context)

    bill_history = Bill.objects.filter(customer=customer).exclude(id=bill.id).order_by('-reading_date')[:10]

    context = {
        'employee': employee,
        'bill': bill,
        'bill_history': bill_history,
        'today': date.today(),
        'customer': customer,
    }
    return render(request, 'bill_preview.html', context)


@employee_session_required
def emp_bill(request, pre_bill_id):
    employee = request.employee
    employee = Employee.objects.get(id=employee.id)
    
    try:
        pre_bill = previewreadings.objects.get(id=pre_bill_id)
    except previewreadings.DoesNotExist:
        messages.error(request, 'Bill preview not found.')
        return redirect('meter_reading')
    
    # Get historical bills for the same customer (excluding the current one)
    # Order by reading date descending to show latest first
    history_bills = previewreadings.objects.filter(
        Customer=pre_bill.Customer
    ).exclude(id=pre_bill_id).order_by('-reading_date')[:10]  # Last 10 bills
    
    context = {
        'employee': employee,
        'pre_bill': pre_bill,
        'history_bills': history_bills
    }
    
    return render(request, 'emp_bill_review.html', context) 

@employee_session_required
def emp_bills_list(request):
    pre_bills = previewreadings.objects.all().order_by('-reading_date')[:20]
    return render(request, 'emp_bill_list.html', {'pre_bills': pre_bills}) 


def user_logout(request): 
    logout(request)
    return redirect('index')