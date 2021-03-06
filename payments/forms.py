from django import forms

from payments.models import Payment


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Payment
        fields = ['user', 'event_type', 'amount', 'initial_usages']
