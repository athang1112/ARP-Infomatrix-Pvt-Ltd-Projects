from django import forms

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(label='Upload Audio File', widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'}))
