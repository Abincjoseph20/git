from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name','phone_number','qualification','file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not (file.name.endswith('.docx') or file.name.endswith('.pdf')):
            raise forms.ValidationError("Only .docx and .pdf files are supported.")
        return file
