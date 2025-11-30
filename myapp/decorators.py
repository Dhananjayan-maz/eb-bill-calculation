# myapp/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .models import *

def employee_session_required(view_func):
    """
    Check session for 'employee_id'. If present, attach `request.employee`
    and call the view. Otherwise redirect to employee_login with ?next=...
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        emp_id = request.session.get('employee_id')
        if emp_id:
            try:
                request.employee = Employee.objects.get(id=emp_id)
            except Employee.DoesNotExist:
                # invalid id in session -> clear and redirect
                request.session.pop('employee_id', None)
                login_url = reverse('employee_login')
                return redirect(f"{login_url}?next={request.path}")
            return view_func(request, *args, **kwargs)

        # Not logged in: redirect to login and preserve next
        login_url = reverse('employee_login')
        next_url = request.path
        # avoid open redirect by ensuring next_url is safe (relative paths are safe)
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = '/'
        return redirect(f"{login_url}?next={next_url}")
    return _wrapped


def customer_session_required(view_func):
    """
    Check session for 'customer_id'. If present, attach `request.customer`
    and call the view. Otherwise redirect to customer_login with ?next=...
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        cust_id = request.session.get('customer_id')
        if cust_id:
            try:
                request.customer = Customer.objects.get(id=cust_id)
            except Customer.DoesNotExist:
                # invalid id in session -> clear and redirect
                request.session.pop('customer_id', None)
                login_url = reverse('customer_login')
                return redirect(f"{login_url}?next={request.path}")
            return view_func(request, *args, **kwargs)

        # Not logged in: redirect to login and preserve next
        login_url = reverse('customer_login')
        next_url = request.path
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = '/'
        return redirect(f"{login_url}?next={next_url}")
    return _wrapped