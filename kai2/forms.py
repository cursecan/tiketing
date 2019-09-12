from django import forms

from .models import (
    Passenger,
)

# class KeretaSearchForm(forms.Form):
#     origin = forms.Field()
#     destination = forms.Field()
#     departdate = forms.DateField()


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            'passenger_nm',
            'passenger_identity',
        ]