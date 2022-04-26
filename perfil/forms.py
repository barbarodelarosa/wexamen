from django import forms

from .models import AffiliateApplication, Profile


class AffiliateApplicationForm(forms.ModelForm):

    profile = forms.ModelChoiceField(queryset = Profile.objects.none(),label="Perfil", required=False)
    # aprovated = forms.BooleanField(initial=False)

    class Meta:
        model = AffiliateApplication
        fields = []

class PagarPlanForm(forms.Form):
    title = forms.CharField()
    description = forms.Textarea()
    price = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        super(PagarPlanForm, self).__init__(*args, **kwargs)
      