from django import forms


class PagarPlanForm(forms.Form):
    title = forms.CharField()
    description = forms.Textarea()
    price = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        super(PagarPlanForm, self).__init__(*args, **kwargs)
      