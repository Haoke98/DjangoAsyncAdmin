from django.forms import ModelForm


def create_dynamic_model_form(**kwargs):
    """动态生成ModelForm"""

    class Meta:
        model = kwargs.get('model')
        fields = kwargs.get('fields')

    
    dynamic_form = type('DynamicModelForm', (ModelForm,), {'Meta': Meta})
    return dynamic_form
