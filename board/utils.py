from datetime import datetime
from uuid import uuid4
from django.db import connections


def dict_fetchall(sql, using='mariaDB'):
    with connections[using].cursor() as cursor:
        cursor.execute(sql)
        desc = cursor.description
        dict_list = []
        for row in cursor.fetchall():
            row = html_text_cont_change(row)
            zip_result = zip([col[0] for col in desc], row)
            dict_list.append(dict(zip_result))
        return dict_list


def html_text_cont_change(row):
    tuple_text = ''
    for index, value in enumerate(row):
        if type(value) == str:
            text_temp = value.replace('&lt;p&gt;', '<p>').replace('&lt;/p&gt;', '</p>').replace('&lt;br&gt;', '<br>')
        else:
            text_temp = str(value)
        if index < len(row)-1:
            text_temp = text_temp + ', '
        tuple_text = tuple_text + str(text_temp)
    re_row = tuple(map(str, tuple_text.split(', ')))
    return re_row


def image_path_rename(filename):
    ext = filename.split('.')[-1]
    now = datetime.now()
    this_time = now.strftime('%Y%m%d%H%M%S')
    time_uuid = this_time + '_' + uuid4().hex
    file_trance_name = '{}.{}'.format(time_uuid, ext)
    return file_trance_name
