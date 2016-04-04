# _*_coding:utf-8_*_
__author__ = 'Alex Li'

from django.core.exceptions import ObjectDoesNotExist


class ClassGrade(object):
    def __init__(self, class_obj):
        self.class_obj = class_obj
        self.errors = []
        self.stu_lack_check_record = set([])  # all the stu lack course check in record will be stored in here

    def fetch_grades(self):
        class_grade_list = []
        days = self.class_obj.courserecord_set.select_related()
        stu_list = self.class_obj.customer_set.select_related()
        for stu in stu_list:
            single_stu_grades = [[stu, 0]]  # 0 stands for the total score ,later will replace it
            total_scores = 0
            for day in days:
                try:
                    day_grade = day.studyrecord_set.select_related().get(student_id=stu.id)
                    single_stu_grades.append([day_grade.get_score_display(), day_grade.color_dic[day_grade.score]])
                    if day_grade.score != -1:  # -1 == D
                        total_scores += day_grade.score
                except  ObjectDoesNotExist as e:
                    self.errors.append(u"student [%s] id[%s] 没查询到第[%s]节的上课纪录" % (stu.name, stu.id, day))
                    self.stu_lack_check_record.add(str(stu.id))
            # print(self.errors)
            single_stu_grades[0][1] = total_scores
            # add each student's whole grades into class_grade_list



            single_stu_grades[0][1] = total_scores
            class_grade_list.append(single_stu_grades)
        return class_grade_list
