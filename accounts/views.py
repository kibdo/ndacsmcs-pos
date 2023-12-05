from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse
import json
# Create your views here.


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def list_users(request):
    users = []
    users.append(
        {'sn': 1, 'user': get_user_model().objects.filter(id=request.user.id).first()})
    count = 2
    for user in get_user_model().objects.all():
        if user.id != request.user.id:
            users.append({'sn': count, 'user': user})
            count += 1
    context = {
        'users': users
    }
    return render(request, 'accounts/list-users.html', context=context)


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def manage_users(request):
    user = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
            print(data['id'])
        if id.isnumeric() and int(id) > 0:
            user = get_user_model().objects.filter(id=id).first()
            print(f'user\'s name is {user.username}')
    context = {
        'user': user
    }
    return render(request, 'accounts/manage-user.html', context)


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def save_user(request):
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = get_user_model().objects.exclude(
            id=id).filter(username=data['username']).all()
    else:
        check = get_user_model().objects.filter(
            username=data['username']).all()
    if len(check) > 0:
        resp['msg'] = "User with thesame Username already exists in the database"
    else:
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0:
                is_staff = None
                is_salesman = None
                user_accnt = get_user_model().objects.filter(
                    id=data['id']).first()
                admin = get_user_model().objects.filter(
                    username='admin').first()
                if 'isAdmin' in data.keys():
                    is_staff = True
                    is_salesman = True
                else:
                    is_staff = False
                if 'isSalesman' in data.keys():
                    is_salesman = True
                else:
                    is_salesman = False
                save_user = get_user_model().objects.filter(id=data['id']).update(
                    first_name=data['firstname'], last_name=data['lastname'], is_salesman=is_salesman, is_staff=is_staff)
                if len(data['password']) > 0:
                    user_object = get_user_model(
                    ).objects.filter(id=data['id']).first()
                    user_object.set_password(data['password'])
                    user_object.save()
            else:
                user_model = get_user_model()
                is_staff = None
                is_salesman = None
                try:
                    if 'isAdmin' in data.keys():
                        is_staff = True
                        is_salesman = True
                    else:
                        is_staff = False
                    if 'isSalesman' in data.keys():
                        is_salesman = True
                    else:
                        is_salesman = False
                except:
                    pass
                save_user = user_model(is_staff=is_staff, is_salesman=is_salesman, username=data['username'],
                                       first_name=data['firstname'], last_name=data['lastname'])
                save_user.set_password(data['password'])

                print('Trial Else')
                save_user.save()

            resp['status'] = 'success'
            messages.success(request, 'User saved successfully.')
        except:
            print('Exception')
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
@user_passes_test(is_admin, redirect_field_name='home-page')
def delete_user(request):
    data = request.POST
    resp = {'status': ''}
    try:
        print('Trial')
        get_user_model().objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'User deleted successfully.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
