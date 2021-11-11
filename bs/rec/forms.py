from django.forms import ModelForm, inlineformset_factory
from .models import Gldetail, Glpost, Entity, Period
# from django.core.files.storage import FileSystemStorage
from crispy_forms.helper import FormHelper
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.shortcuts import render


class GldetailViewForm(forms.ModelForm):

    entity = forms.ModelChoiceField(queryset=Entity.objects.all(), to_field_name='entity', empty_label="Select Entity")
    period = forms.ModelChoiceField(queryset=Period.objects.all(), to_field_name='period')


    class Meta:
        model = Gldetail
        fields = ['entity', 'period']

    def __init__(self, user, *args, **kwargs):
        super(GldetailViewForm, self).__init__(*args, **kwargs)
        if user.is_active:
            self.fields['entity'].queryset = Entity.objects.filter(users=user)

class StatusViewForm(forms.ModelForm):
    period = forms.ModelChoiceField(queryset=Period.objects.all(), to_field_name='period')

    class Meta:
        model = Gldetail
        fields = ('period',)

    def __init__(self, *args, **kwargs):
        super(StatusViewForm, self).__init__(*args, **kwargs)

class GldetailForm(ModelForm):

    def __init__(self, *args, **kwargs):    

        super(GldetailForm, self).__init__(*args, **kwargs)
        self.fields['entity'].widget.attrs['disabled'] = True
        self.fields['period'].widget.attrs['disabled'] = True
        self.fields['glnum'].widget.attrs['readonly'] = True
        self.fields['gldesc'].widget.attrs['readonly'] = True
        
    class Meta:
        model = Gldetail
        fields = '__all__'
        
class GlpostForm(ModelForm):

    class Meta:
        model = Glpost
        exclude = ()
    
    def __init__(self, *args, **kwargs):
        super(GlpostForm, self).__init__(*args, **kwargs)
        self.fields['jdate'].widget.attrs['style'] = "width: 110px"
        self.fields['jdate'].widget.attrs['placeholder'] = "mm/dd/yyyy"
        self.fields['jdate'].widget.attrs['minlength'] = "10"
        self.fields['jref'].widget.attrs['style'] = "width: 80px"
        self.fields['jref'].widget.attrs['placeholder'] = "123456"
        self.fields['jref'].widget.attrs['minlength'] = "6"
        self.fields['jamt'].widget.attrs['style'] = "width: 140px"
        self.fields['jamt'].widget.attrs['class'] = "text-right"
        self.fields['jdesc'].widget.attrs['style'] = "width: 200px"
        self.fields['jdesc'].widget.attrs['minlength'] = "2"

GlpostFormSet = inlineformset_factory(Gldetail, Glpost, form=GlpostForm, extra=1)