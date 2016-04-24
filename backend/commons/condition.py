#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
from django.db.models import Q

def search_condition_create(conditions):
    con = Q()
    for k, v in conditions.items():
        temp = Q()
        temp.connector = 'OR'
        for item in v:
            temp.children.append((k, item))
        con.add(temp, 'OR')
    return con

def search_condition_add(con,conditions):
    for k, v in conditions.items():
        temp = Q()
        temp.connector = 'OR'
        for item in v:
            temp.children.append((k, item))
        con.add(temp, 'OR')
    return con

def main():
    pass


if __name__ == '__main__':
    main()
