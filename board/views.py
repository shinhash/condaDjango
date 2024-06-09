from math import ceil
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from board.utils import *

import logging
logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'post/views/index.html')


def post_list(request):
    page_num = request.POST.get('page_num')
    if page_num is None or page_num == '':
        page_num = 1

    view_cnt = request.POST.get('view_cnt')
    if view_cnt is None or view_cnt == '':
        view_cnt = 10

    page_num = int(page_num)
    view_cnt = int(view_cnt)

    query_params = {
        'query_id': 'selectPostCount',
        'board_id': 'BD001',
    }
    sql = render_to_string('post/model/sql/post.sql', query_params)
    post_cnt = dict_fetchall(sql)[0].get('POST_CNT')
    post_cnt = int(post_cnt)

    logger.debug('sql : ' + str(sql))

    page_num_limit = (page_num - 1) * view_cnt
    query_params = {
        'query_id': 'selectPostList',
        'board_id': 'BD001',
        'page_num_limit': page_num_limit,
        'view_cnt': view_cnt
    }
    sql = render_to_string('post/model/sql/post.sql', query_params)
    result = dict_fetchall(sql)
    page_len = ceil(post_cnt / view_cnt)

    logger.debug('sql : ' + str(sql))
    logger.debug('result : ' + str(result))

    logger.debug('page_num : ' + str(page_num))
    logger.debug('view_cnt : ' + str(view_cnt))
    logger.debug('page_len = ' + str(page_len))

    context = {
        'post_list': result,
        'page_num': page_num,
        'post_cnt': post_cnt,
        'page_len': page_len,
        'post_all_cnt': post_cnt,
    }
    return render(request, 'post/views/post_list.html', context)


def post_create(request):
    if request.method == 'POST':
        file_origin_name = ''
        file_trance_name = ''
        image_view_path = ''

        if request.FILES:
            my_file = request.FILES['image']
            fs = FileSystemStorage(location='media/images/', base_url='media/images/')

            file_origin_name = my_file.name
            file_trance_name = image_path_rename(my_file.name)
            fs.save(file_trance_name, my_file)
            image_view_path = '/media/images/' + file_trance_name

        query_params = {
            'query_id': 'generatePostId',
            'board_id': 'BD001',
        }
        sql = render_to_string('post/model/sql/post.sql', query_params)
        post_id = dict_fetchall(sql)[0].get('POST_ID')
        logger.debug('sql : ' + str(sql))
        logger.debug('post_id : ' + str(post_id))

        post_title = request.POST.get('post_title')
        post_cont = request.POST.get('post_cont')
        logger.debug('post_cont : ' + str(post_cont))

        query_params = {
            'query_id': 'insertPost',
            'board_id': 'BD001',
            'post_id': post_id,
            'post_title': post_title,
            'post_cont': post_cont,
            'file_origin_name': file_origin_name,
            'file_trance_name': file_trance_name,
            'image_view_path': image_view_path
        }
        sql = render_to_string('post/model/sql/post.sql', query_params)
        logger.debug('sql : ' + str(sql))
        result = dict_fetchall(sql)

        context = {
            'result': 'SUCCESS',
            'post_id': post_id,
        }
        return JsonResponse(context)
    context = {}
    return render(request, 'post/views/post_create.html', context)


def post_detail(request):
    if request.method == 'POST':
        detail_post_id = request.POST.get('post_id')
        view_type = request.POST.get('view_type')

        logger.debug('detail_post_id = ' + str(detail_post_id))
        logger.debug('view_type = ' + str(view_type))

        query_params = {
            'query_id': 'selectPostDetail',
            'board_id': 'BD001',
            'post_id': detail_post_id
        }
        sql = render_to_string('post/model/sql/post.sql', query_params)
        logger.debug('sql : ' + str(sql))
        result = dict_fetchall(sql)[0]
        logger.debug('result : ' + str(result))
        context = {
            'post': result
        }
        if view_type == 'detail':
            return render(request, 'post/views/post_detail.html', context)
        elif view_type == 'update':
            return render(request, 'post/views/post_update.html', context)

    return redirect('post/list')


def post_update(request):
    if request.method == 'POST':

        file_origin_name = ''
        file_trance_name = ''
        image_view_path = ''

        if request.FILES:
            my_file = request.FILES['image']
            fs = FileSystemStorage(location='media/images/', base_url='media/images/')

            file_origin_name = my_file.name
            file_trance_name = image_path_rename(my_file.name)
            fs.save(file_trance_name, my_file)
            image_view_path = '/media/images/' + file_trance_name

        post_id = request.POST.get('post_id')
        logger.debug('post_id : ' + str(post_id))
        post_cont = request.POST.get('post_cont')
        logger.debug('post_cont : ' + str(post_cont))

        query_params = {
            'query_id': 'updatePost',
            'board_id': 'BD001',
            'post_id': post_id,
            'post_cont': post_cont,
            'file_origin_name': file_origin_name,
            'file_trance_name': file_trance_name,
            'image_view_path': image_view_path
        }
        sql = render_to_string('post/model/sql/post.sql', query_params)
        logger.debug('update sql : ' + str(sql))
        result = dict_fetchall(sql)

        context = {
            'result': 'SUCCESS',
            'post_id': post_id
        }
        return JsonResponse(context)
    return redirect('post/list')

