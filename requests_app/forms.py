from django import forms
from .models import Requestor, Antibody, Study, Tissue, Request, Status, Assignee, Probe, Priority

class RequestForm(forms.ModelForm):
    special_request = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}), required=False, max_length=256)
    
    class Meta:
        model = Request
        fields = ['requestor', 'antibody', 'probe', 'study', 'description', 'tissue', 'priority', 'special_request', 'assigned_to']
        widgets = {
            'requestor': forms.Select(attrs={'class': 'form-control'}),
            'antibody': forms.Select(attrs={'class': 'form-control'}),
            'probe': forms.Select(attrs={'class': 'form-control'}),
            'study': forms.Select(attrs={'class': 'form-control'}),
            'tissue': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requestor'].queryset = Requestor.objects.all().order_by('name')
        self.fields['antibody'].queryset = Antibody.objects.all().order_by('name')
        self.fields['antibody'].label_from_instance = lambda obj: f"{obj.name} - {obj.description}"
        self.fields['probe'].queryset = Probe.objects.all().order_by('name')
        self.fields['probe'].label_from_instance = lambda obj: f"{obj.name} - {obj.description}"
        self.fields['study'].queryset = Study.objects.all().order_by('study_id')
        self.fields['tissue'].queryset = Tissue.objects.all().order_by('name')
        self.fields['priority'].queryset = Priority.objects.all().order_by('value')
        self.fields['assigned_to'].queryset = Assignee.objects.all().order_by('name')
        self.fields['assigned_to'].required = False
        self.fields['probe'].required = False

class RequestEditForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 256}), required=False, max_length=256)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}), required=False, max_length=256)
    
    class Meta:
        model = Request
        fields = ['status', 'notes', 'description', 'special_request', 'priority', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 256}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all().order_by('status')
        self.fields['priority'].queryset = Priority.objects.all().order_by('value')
        self.fields['assigned_to'].queryset = Assignee.objects.all().order_by('name')
        self.fields['assigned_to'].required = False

class RequestSearchForm(forms.Form):
    request_id = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Request ID'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    requestor = forms.ModelChoiceField(queryset=Requestor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    antibody = forms.ModelChoiceField(queryset=Antibody.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    probe = forms.ModelChoiceField(queryset=Probe.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    tissue = forms.ModelChoiceField(queryset=Tissue.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    study = forms.ModelChoiceField(queryset=Study.objects.all().order_by('study_id'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all().order_by('status'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    priority = forms.ModelChoiceField(queryset=Priority.objects.all().order_by('value'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    assigned_to = forms.ModelChoiceField(queryset=Assignee.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    special_request = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Special Request'}))
    notes = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notes'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up label_from_instance for better display
        self.fields['antibody'].label_from_instance = lambda obj: f"{obj.name} - {obj.description}"
        self.fields['probe'].label_from_instance = lambda obj: f"{obj.name} - {obj.description}"
        
        # Add empty choice to all ModelChoiceFields
        self.fields['requestor'].empty_label = "Select Requestor"
        self.fields['antibody'].empty_label = "Select Antibody"
        self.fields['probe'].empty_label = "Select Probe"
        self.fields['tissue'].empty_label = "Select Tissue"
        self.fields['study'].empty_label = "Select Study"
        self.fields['status'].empty_label = "Select Status"
        self.fields['priority'].empty_label = "Select Priority"
        self.fields['assigned_to'].empty_label = "Select Assignee"
        


class StudyEditForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ['study_id', 'title']
        widgets = {
            'study_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

class AntibodyForm(forms.ModelForm):
    class Meta:
        model = Antibody
        fields = ['name', 'description', 'antigen', 'species', 'recognizes', 'vendor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'antigen': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'species': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'recognizes': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'vendor': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

class RequestorForm(forms.ModelForm):
    class Meta:
        model = Requestor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

class TissueForm(forms.ModelForm):
    class Meta:
        model = Tissue
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status']
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

class AssigneeForm(forms.ModelForm):
    class Meta:
        model = Assignee
        fields = ['name', 'email', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['value', 'label', 'description']
        widgets = {
            'value': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 50}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
        }

class ProbeForm(forms.ModelForm):
    class Meta:
        model = Probe
        fields = ['name', 'description', 'sequence', 'target_gene', 'vendor', 'catalog_number', 'platform', 'target_region', 'number_of_pairs']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'sequence': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 500}),
            'target_gene': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'vendor': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'catalog_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
            'platform': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'target_region': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'number_of_pairs': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        } 