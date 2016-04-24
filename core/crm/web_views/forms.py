# _*_coding:utf-8_*_
__author__ = 'Alex Li'

from django.forms import ModelForm, Textarea

from core.crm.web_models.models import Compliant


class CompliantForm(ModelForm):
    class Meta:
        model = Compliant
        fields = (
            'title',
            'compliant_type',
            'content',
            'name'
        )

        widgets = {
            'content': Textarea(
                attrs={
                    'cols': 100,
                    'rows': 10,
                    'name': 'content',
                    'class': 'form-control',
                    'placeholder': u"描述需达到15字以上..."
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CompliantForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {
                'class': 'form-control input-lg',
                'name': 'title'
            }
        )
        self.fields['compliant_type'].widget.attrs.update(
            {
                'class': 'form-control'
            }
        )
        self.fields['name'].widget.attrs.update(
            {
                'class': 'form-control input-sm',
                'placeholder': u"请留下您的姓名,若想匿名则可不填..."
            }
        )
