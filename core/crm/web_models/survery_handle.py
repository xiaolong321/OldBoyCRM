# _*_coding:utf-8_*_
__author__ = 'Alex Li'

from django.db.models import Sum, Count

import models


class Survery(object):
    def __init__(self, client_id, survery_id, data):
        self.data = data
        self.survery_id = survery_id
        self.errors = {}
        self.client_id = client_id

    def is_valid(self):
        # print()
        record_exist = models.SurveryRecord.objects.filter(survery_id=self.survery_id, client_id=self.client_id)
        print('=--->', record_exist)
        if record_exist:
            self.errors["record_exist"] = u"问卷已生成,请勿重复提交!"
            return False

        return True

    def handle(self):
        for question_id, val in self.data.items():
            if question_id != 'username':
                models.SurveryRecord.objects.create(
                    survery_id=self.survery_id,
                    student_name=self.data["username"],
                    survery_item_id=question_id,
                    score=val["score"],
                    suggestion=val["suggestion"],
                    client_id=self.client_id

                )

    def save(self):
        obj = self.handle()
        # pass


def generate_chart_data(survery_obj):
    survery_records = survery_obj.surveryrecord_set.select_related()
    # for record in survery_records:
    sum_list = models.SurveryRecord.objects.filter(survery_id=survery_obj.id, survery_item__anwser_type='score').values(
        "survery__id", "survery_item__name", "survery_item_id").annotate(score_sum=Sum("score"),
                                                                         survery_count=Count('score'))
    for item in sum_list:
        print(item)

    data_dic = {'category': [x['survery_item__name'] for x in sum_list],
                'data': [x['score_sum'] / x["survery_count"] for x in sum_list]
                }

    return data_dic
