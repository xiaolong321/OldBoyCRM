#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import json
import logging
from django.core import serializers
from django.shortcuts import HttpResponse
from backend.commons import serialization

logger = logging.getLogger(__name__)
from ..admin import models_message

Models = models_message.MyMessage
Constants_MailStatus = models_message.MailStatus


def Message(request):
    """
        Message 分离器
    """
    if request.method == 'GET':
        return get_message(request)
    elif request.method == 'POST':
        return post_message(request)
    else:
        return HttpResponse({})


def get_message(request):
    logger.debug(
        u'#' * 25 + u'get_message' + u'#' * 15 +
        u'进行get 模式操作 开始'
    )
    ret = {"count": 0, "ret_code": 1, "results": [], "action": "get_message"}
    try:
        messages = Models.objects.filter(
            receive_user=request.user,
            Status=0
        ).order_by("-updated_at")
    except Exception as e:
        logger.error(
            u'#' * 20 + u'get_message' + u'#' * 15 +
            u'获取 原始数据失败 开始采用默认数据 %s' % e
        )
        messages = json.dumps([])
    ret['results'] = serializers.serialize(
        "json",
        messages
    )
    ret['count'] = len(messages)
    ret['ret_code'] = 0
    logger.debug(
        u'#' * 25 + u'get_message' + u'#' * 15 +
        u'进行get 模式操作 结束'
    )
    return HttpResponse(json.dumps(ret, cls=serialization.CJsonEncoder))


def post_message(request):
    logger.debug(
        u'#' * 25 + u'post_message' + u'#' * 15 +
        u'进行 post 模式操作 开始'
    )
    ret = {"ret_code": 1, "action": "post_message"}
    try:
        mode = request.POST.get('mode', None)
        if mode is None:
            raise Exception(u'模式获取失败')
        if mode == 'read':
            ret = post_message_READ(request, ret)
        elif mode == 'draft':
            ret = post_message_DRAFT(request, ret)
        elif mode == 'trash':
            ret = post_message_TRASH(request, ret)
        elif mode == 'deleted':
            ret = post_message_DELETED(request, ret)
        elif mode == 'add':
            ret = post_message_UNREAD(request, ret)
        else:
            raise Exception(u'未知模式')
        logger.debug(
            u'#' * 25 + u'post_message' + u'#' * 15 +
            u'进行 post 模式操作 结束'
        )
    except Exception as e:
        logger.error(
            u'#' * 25 + u'post_message' + u'#' * 15 +
            u'进行 post 模式操作 异常 %s' % e.message
        )
        ret['message'] = e.message
    return HttpResponse(json.dumps(ret))


def post_message_READ(request, ret):
    logger.debug(
        u'#' * 35 +
        u'进行 read 模式操作 开始'
    )
    pk = request.POST.get('pk', None)
    if pk is None:
        raise Exception(u' pk 值 不能为空')
    pk = json.loads(pk)
    if type(pk) != list:
        pks = [pk]
    else:
        pks = pk
    ret["results"] = []
    Message_Status(pks=pks, ret=ret, Status=Constants_MailStatus.READ)
    logger.debug(
        u'#' * 35 +
        u'进行 read 模式操作 结束'
    )
    ret["ret_code"] = 0
    ret["message"] = u'修改成功'
    return ret


def post_message_DRAFT(request, ret):
    logger.debug(
        u'#' * 35 +
        u'进行 DRAFT 模式操作 开始'
    )
    pk = request.POST.get('pk', None)
    if pk is None:
        raise Exception(u' pk 值 不能为空')

    pk = json.loads(pk)
    if type(pk) != list:
        pks = [pk]
    else:
        pks = pk
    ret["results"] = []
    Message_Status(pks=pks, ret=ret, Status=Constants_MailStatus.READ)
    ret["ret_code"] = 0
    ret["message"] = u'修改成功'
    logger.debug(
        u'#' * 35 +
        u'进行 DRAFT 模式操作 结束'
    )
    return HttpResponse()


def post_message_TRASH(request, ret):
    logger.debug(
        u'#' * 35 +
        u'进行 TRASH 模式操作 开始'
    )
    pk = request.POST.get('pk', None)
    if pk is None:
        raise Exception(u' pk 值 不能为空')

    pk = json.loads(pk)
    if type(pk) != list:
        pks = [pk]
    else:
        pks = pk
    ret["results"] = []
    Message_Status(pks=pks, ret=ret, Status=Constants_MailStatus.READ)
    ret["ret_code"] = 0
    ret["message"] = u'修改成功'
    logger.debug(
        u'#' * 35 +
        u'进行 TRASH 模式操作 结束'
    )
    return HttpResponse()


def post_message_DELETED(request, ret):
    logger.debug(
        u'#' * 35 +
        u'进行 DELETED 模式操作 开始'
    )
    pk = request.POST.get('pk', None)
    if pk is None:
        raise Exception(u' pk 值 不能为空')

    pk = json.loads(pk)
    if type(pk) != list:
        pks = [pk]
    else:
        pks = pk
    ret["results"] = []
    Message_Status(pks=pks, ret=ret, Status=Constants_MailStatus.READ)
    ret["ret_code"] = 0
    ret["message"] = u'修改成功'
    logger.debug(
        u'#' * 35 +
        u'进行 DELETED 模式操作 结束'
    )
    return HttpResponse()


def post_message_UNREAD(request, ret):
    logger.debug(
        u'#' * 35 +
        u'进行 UNREAD 模式操作 开始'
    )
    type = request.POST.get(u'type', u'info')
    size = request.POST.get(u'size', u'large')
    delay = request.POST.get(u'delay', 15000)
    title = request.POST.get(u'title', type)
    msg = request.POST.get(u'msg', None)
    models = request.POST.get(u'models', '')
    receive_user = request.POST.get(u'receive_user', None)
    creator = request.POST.get(u'creator', request.user.id)
    if receive_user is None:
        raise Exception(u'请提供 接收人')
    if msg is None:
        raise Exception(u'消息不能为空')
    if len(msg) == 0:
        raise Exception(u'消息不能为空')
    logger.debug(
        u'#' * 25 +
        u'receive_user:%s creator:%s type:%s size:%s delay:%s title:%s msg:%s ' % (
            receive_user,
            creator,
            type,
            size,
            delay,
            title,
            msg,
        )

    )
    try:
        receive_user = models_message.UserProfile.objects.get(id=receive_user)
    except Exception as e:
        raise Exception(u'receive_user 用户转换失败 ')
    try:
        creator = models_message.UserProfile.objects.get(id=creator)
    except Exception as e:
        raise Exception(u'creator 用户转换失败 ')
    Models.objects.create(
        receive_user=receive_user,
        creator=creator,
        Status=Constants_MailStatus.UNREAD,
        Message=json.dumps(
            {
                u'type': type,
                u'size': size,
                u'delay': delay,
                u'title': title,
                u'msg': msg,
                u'models': models,
            }
        )
    )
    ret["ret_code"] = 0
    ret["message"] = u'添加消息成功'
    logger.debug(
        u'#' * 35 +
        u'进行 UNREAD 模式操作 结束'
    )
    return ret


def Message_Status(pks, ret, Status):
    error_count = 0
    for pk_id in pks:
        try:
            logger.debug(
                u'#' * 5 +
                u'对 id:%s 操作 消息 状态 %s 开始' % (
                    pk_id,
                    Status,
                )
            )
            message = Models.objects.get(id=pk_id)
            message.Status = Status
            message.save()
            ret["results"].append(
                {'pk': pk_id, 'status': Status, 'code': 0}
            )
            logger.debug(
                u'#' * 5 +
                u'对 id:%s 操作 消息 状态 %s 结束' % (
                    pk_id,
                    Status,
                )
            )
        except Exception as e:
            error_count += 1
            ret["results"].append(
                {'pk': pk_id, 'status': Constants_MailStatus.READ, 'code': 1}
            )
            logger.error(
                u'#' * 5 +
                u'对 id:%s 操作 消息 状态 %s 失败 %s' % (
                    pk_id,
                    Status,
                    e.message,
                )
            )
    ret["error_count"] = error_count


def main():
    pass


if __name__ == '__main__':
    main()
