import csv
from django.utils.encoding import smart_str
from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
from flask import jsonify
from .models import Category, Products, Sales, salesItems, Settings
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
import json
import sys
from datetime import date, datetime
from django.core.paginator import Paginator
from .filters import SalesFilter
# if admin user


def is_admin(user):
    return user.is_staff


def is_salesman(user):
    return user.is_salesman


def is_salesman_or_is_admin(user):
    if user.is_salesman or user.is_staff:
        return True
    return False

# Login


def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')

# Logout


def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.


@login_required
def home(request):
    settings = Settings.objects.all()
    if len(settings) <= 0:
        Settings(interest_rate=9).save()
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total', flat=True))
    context = {
        'page_title': 'Home',
        'categories': categories,
        'products': products,
        'transaction': transaction,
        'total_sales': total_sales,
    }
    return render(request, 'posApp/home.html', context)


def about(request):
    context = {
        'page_title': 'About',
    }
    return render(request, 'posApp/about.html', context)

# Categories


@login_required
def category(request):
    category_list = Category.objects.all()
    # category_list = {}
    context = {
        'page_title': 'Category List',
        'category': category_list,
    }
    return render(request, 'posApp/category.html', context)


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()

    context = {
        'category': category
    }
    return render(request, 'posApp/manage_category.html', context)


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def save_category(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_category = Category.objects.filter(id=data['id']).update(
                name=data['name'], description=data['description'], status=data['status'])
        else:
            save_category = Category(
                name=data['name'], description=data['description'], status=data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def delete_category(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Category.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Products


@login_required
def products(request):
    product_list = Products.objects.all()
    total_stock_price_worth = 0
    for product in product_list:
        total_stock_price_worth += product.total_stock_price
    context = {
        'page_title': 'Product List',
        'products': product_list,
        'total_stock_price_worth': total_stock_price_worth
    }
    return render(request, 'posApp/products.html', context)


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()

    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'posApp/manage_product.html', context)


def test(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'posApp/test.html', context)


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def save_product(request):
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0:
        resp['msg'] = "Product Brand Already Exists in the database"
    else:
        category = Category.objects.filter(id=data['category_id']).first()
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0:
                save_product = Products.objects.filter(id=data['id']).update(
                    code=data['code'], category_id=category, name=data['name'], units=data['units'], description=data['description'], price=int(data['price']), status=data['status'])
            else:
                save_product = Products(code=data['code'], category_id=category, units=data['units'], name=data['name'],
                                        description=data['description'], price=int(data['price']), status=data['status'])
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def delete_product(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Products.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
@user_passes_test(is_salesman_or_is_admin, redirect_field_name='home-page')
def pos(request):
    products = Products.objects.filter(status=1)
    product_json = []
    for product in products:
        product_json.append(
            {'id': product.id, 'name': product.name, 'price': int(product.price)})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json)
    }
    # return HttpResponse('')
    return render(request, 'posApp/pos.html', context)


@login_required
@user_passes_test(is_salesman_or_is_admin, redirect_field_name='home-page')
def checkout_modal(request):
    grand_total = 0
    interest_rate = Settings.objects.all().last().interest_rate
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total': grand_total,
        'interest_rate': interest_rate}
    return render(request, 'posApp/checkout.html', context)


@login_required
@user_passes_test(is_salesman_or_is_admin, redirect_field_name='home-page')
def save_pos(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code=str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        client_name_length = len(data['client_name'])
        coorp_number_length = len(data['coorp_number'])

        if client_name_length > 0 and coorp_number_length > 0:
            tendered_amount = int(data['grand_total'])
            interest_rate = Settings.objects.last().interest_rate
            interest = (interest_rate/100) * int(data['sub_total'])
            interest = round(interest)
            grand_total = interest + int(data['grand_total'])
            grand_total = round(grand_total)
            tendered_amount = grand_total

            sales = Sales(interest_rate=interest_rate, interest=interest, is_credit=True, cooperative_number=data['coorp_number'], client_name=data['client_name'], code=code, sub_total=data['sub_total'], tax=0, tax_amount=0,
                          grand_total=grand_total, tendered_amount=tendered_amount, amount_change=data['amount_change']).save()
        else:
            print('hello')
            sales = Sales(interest_rate=0, interest=0, is_credit=False, cooperative_number=data['coorp_number'], client_name=data['client_name'], code=code, sub_total=data['sub_total'], tax=0, tax_amount=0,
                          grand_total=data['grand_total'], tendered_amount=data['tendered_amount'], amount_change=data['amount_change']).save()
        sale_id = Sales.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i]
            price = data.getlist('price[]')[i]
            print(product.units)
            total = float(qty) * int(price)
            print({'sale_id': sale, 'product_id': product,
                  'qty': qty, 'price': price, 'total': total})
            salesItems(sale_id=sale, product_id=product,
                       qty=qty, price=price, total=total).save()
            i += int(1)
            # No. of units remaining
            units_remaining = int(product.units) - float(qty)
            Products.objects.filter(id=product_id).update(
                units=units_remaining)
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def salesList(request):
    enumeration = []
    sales = Sales.objects.all().order_by('pk').reverse()
    for sale in sales:
        print(sale.id)
    sale_items = salesItems.objects.all()
    sale_data = []
    grand_total_sales = 0
    date_range = {
        'start': None,
        'end': None
    }
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        data['items'] = salesItems.objects.filter(sale_id=sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(int(data['tax_amount']), '.2f')
    sale_data = SalesFilter(request.GET, queryset=sales)
    total = 0
    for completed_sale in sale_data.qs:
        total += 1
        grand_total_sales += completed_sale.grand_total
    print(total)
    # Assigning S/N
    for sale_sn, sale_obj in enumerate(sale_data.qs, 1):
        enumeration.append([sale_sn, sale_obj.code])
    # Paginator
    sale_data = Paginator(sale_data.qs, 700)
    page_number = request.GET.get('page')
    sale_data = sale_data.get_page(page_number)

    # Filter
    date_range['end'] = request.GET.get('date_after')
    date_range['start'] = request.GET.get('date_before')
    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
        'grand_total_sales': grand_total_sales,
        'date_range': date_range,
        'sale_items': sale_items,
        'enumeration': enumeration
    }
    # return HttpResponse('')
    return render(request, 'posApp/sales.html', context)


@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id=id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales, field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id=sales).all()
    context = {
        "transaction": transaction,
        "salesItems": ItemList
    }

    return render(request, 'posApp/receipt.html', context)
    # return HttpResponse('')


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def delete_sale(request):
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id=id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def settings(request):
    settings = Settings.objects.all()
    if len(settings) <= 0:
        Settings(interest_rate=9).save()
    int_rate = Settings.objects.last().interest_rate
    if request.method == 'POST':
        data = request.POST
        interest_rate = data.get('interest_rate')
        print(interest_rate)
        save_settings = Settings.objects.all().last()
        save_settings.interest_rate = int(interest_rate)
        save_settings.save()
        int_rate = Settings.objects.last().interest_rate
        messages.success(request, 'Settings Updated Successfully')
    context = {
        'interest_rate': int_rate
    }
    return render(request, 'posApp/settings.html', context=context)


@login_required
def download_sales(request):
    sales = Sales.objects.all().order_by('pk').reverse()
    sale_data = SalesFilter(request.GET, queryset=sales)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"S/N"),
        smart_str(u"DateTime"),
        smart_str(u"Transaction code"),
        smart_str(u"Customer's Name"),
        smart_str(u"Cooperative Number"),
        smart_str(u"Items"),
        smart_str(u"Sub Total"),
        smart_str(u"Interest"),
        smart_str(u"Total")
    ])
    serial_number = 0
    for sale in sale_data.qs:
        serial_number += 1
        items = ''
        for item in salesItems.objects.all():
            if item.sale_id.code == sale.code:
                items += f'{item.product_id.name}, '
        writer.writerow([
            smart_str(serial_number),
            smart_str(sale.date_created),
            smart_str(sale.code),
            smart_str(sale.client_name),
            smart_str(sale.cooperative_number),
            smart_str(items[:-2]),
            smart_str(sale.sub_total),
            smart_str(sale.interest),
            smart_str(sale.grand_total)
        ])

    return response
