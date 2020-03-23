from django import forms
from django.core.validators import FileExtensionValidator


class PotholeImageForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg'])],
                           widget=forms.FileInput(attrs={'accept': 'image/jpeg'}),
                           label="Select Pothole image")
