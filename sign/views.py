from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from sign.utils import dict_fetchall

import logging
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, 'sign/views/index.html')


def signin(request):
    if request.method == 'POST':
        sign_id = request.POST.get('sign_id')
        sign_pw = request.POST.get('sign_pw')
        logger.debug('sign_id : ' + str(sign_id))
        logger.debug('sign_pw : ' + str(sign_pw))

        query_params = {
            'query_id': 'selectSignUser',
            'sign_id': sign_id,
        }
        sql = render_to_string('sign/model/sql/sign.sql', query_params)
        logger.debug('sql : ' + str(sql))
        result = dict_fetchall(sql)

        error_code = ''
        sign_result = 'FAIL'

        if result is not None and len(result) > 0:
            if sign_pw == result[0].get('USER_PW'):
                sign_result = 'SUCCESS'
                request.session['sign_session'] = sign_id
            else:
                error_code = 'LOGIN_PW_NE'
        else:
            error_code = 'LOGIN_ID_NE'

        context = {
            'result': sign_result,
            'error_code': error_code,
        }
        return JsonResponse(context)
    return render(request, 'sign/views/signin.html')


def signup(request):
    if request.method == 'POST':
        sign_id = request.POST.get('sign_id')
        sign_pw = request.POST.get('sign_pw')
        name = request.POST.get('nick_name')

        sign_up_result = 'FAIL'
        error_code = 'DUPLE'

        query_params = {
            'query_id': 'selectSignUser',
            'sign_id': sign_id,
        }
        sql = render_to_string('sign/model/sql/sign.sql', query_params)
        dc_result = dict_fetchall(sql)

        if dc_result is None or len(dc_result) == 0:
            error_code = 'ONLY'
            query_params = {
                'query_id': 'insertSignUser',
                'sign_id': sign_id,
                'sign_pw': sign_pw,
                'name': name,
            }
            sql = render_to_string('sign/model/sql/sign.sql', query_params)
            result = dict_fetchall(sql)
            sign_up_result = 'SUCCESS'

        context = {
            'result': sign_up_result,
            'error_code': error_code
        }
        return JsonResponse(context)
    return render(request, 'sign/views/signup.html')


def signout(request):
    if request.session.get('sign_session'):
        del(request.session['sign_session'])

    context = {}
    return redirect('sign/signin')
