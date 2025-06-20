from django import forms
from .models import Requestor, Antibody, Study, Tissue, Request, Status

class RequestForm(forms.ModelForm):
    special_request = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}), required=False)
    
    class Meta:
        model = Request
        fields = ['requestor', 'antibody', 'study', 'description', 'tissue', 'special_request']
        widgets = {
            'requestor': forms.Select(attrs={'class': 'form-control'}),
            'antibody': forms.Select(attrs={'class': 'form-control'}),
            'study': forms.Select(attrs={'class': 'form-control'}),
            'tissue': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requestor'].queryset = Requestor.objects.all()
        self.fields['antibody'].queryset = Antibody.objects.all()
        self.fields['study'].queryset = Study.objects.all()
        self.fields['tissue'].queryset = Tissue.objects.all()

class RequestEditForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status', 'notes', 'description']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 256}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()

class RequestSearchForm(forms.Form):
    request_id = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Request ID'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    requestor = forms.ModelChoiceField(queryset=Requestor.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    tissue = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tissue'}))
    study = forms.ModelChoiceField(queryset=Study.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

class StudyEditForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ['study_id', 'title']
        widgets = {
            'study_id': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        } 