# coding: utf-8
from django.db import connection


def execute_custom_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def dict_fetchall(sql):
    cursor = connection.cursor()
    """将游标返回的结果保存到一个字典对象中"""
    cursor.execute(sql, None)
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
    ]
