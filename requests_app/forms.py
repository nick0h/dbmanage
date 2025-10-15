from django import forms
from .models import Requestor, Antibody, Study, Tissue, Request, Status, Assignee, Probe, Priority, EmbeddingRequest, SectioningRequest

class RequestForm(forms.ModelForm):
    special_request = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}), required=False, max_length=256)
    
    class Meta:
        model = Request
        fields = ['requestor', 'antibody', 'probe', 'study', 'description', 'tissue', 'priority', 'special_request', 'assigned_to', 'links']
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
        self.fields['antibody'].queryset = Antibody.objects.filter(archived=False).order_by('name')
        self.fields['antibody'].label_from_instance = lambda obj: f"{obj.name} - {obj.description}"
        self.fields['probe'].queryset = Probe.objects.filter(archived=False).order_by('name')
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
        fields = ['status', 'notes', 'description', 'special_request', 'priority', 'assigned_to', 'antibody', 'probe']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 256}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'antibody': forms.Select(attrs={'class': 'form-control'}),
            'probe': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all().order_by('status')
        self.fields['priority'].queryset = Priority.objects.all().order_by('value')
        self.fields['assigned_to'].queryset = Assignee.objects.all().order_by('name')
        self.fields['assigned_to'].required = False
        self.fields['antibody'].queryset = Antibody.objects.filter(archived=False).order_by('name')
        self.fields['antibody'].label_from_instance = lambda obj: f"{obj.name} - {obj.description}"
        self.fields['probe'].queryset = Probe.objects.filter(archived=False).order_by('name')
        self.fields['probe'].label_from_instance = lambda obj: f"{obj.name} - {obj.description}"
        self.fields['probe'].required = False

class RequestSearchForm(forms.Form):
    request_id = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Request ID'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    requestor = forms.ModelChoiceField(queryset=Requestor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    antibody = forms.ModelChoiceField(queryset=Antibody.objects.filter(archived=False).order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    probe = forms.ModelChoiceField(queryset=Probe.objects.filter(archived=False).order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
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

# Embedding Request Form
class EmbeddingRequestForm(forms.ModelForm):
    special_request = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}), required=False, max_length=256)
    
    class Meta:
        model = EmbeddingRequest
        fields = ['requestor', 'study', 'special_request', 'assigned_to', 'currently_in', 'take_down_date', 'length_of_time_in_etoh', 'number_of_animals', 'date_of_xylene_etoh_change', 'links']
        exclude = ['tissues']
        widgets = {
            'requestor': forms.Select(attrs={'class': 'form-control'}),
            'study': forms.Select(attrs={'class': 'form-control'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'currently_in': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Currently In'}),
            'take_down_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'length_of_time_in_etoh': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 40}),
            'number_of_animals': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Animals'}),
            'date_of_xylene_etoh_change': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requestor'].queryset = Requestor.objects.all().order_by('name')
        self.fields['study'].queryset = Study.objects.all().order_by('study_id')
        self.fields['assigned_to'].queryset = Assignee.objects.all().order_by('name')
        self.fields['assigned_to'].required = False
        self.fields['take_down_date'].required = False
        self.fields['length_of_time_in_etoh'].required = False
        self.fields['currently_in'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

# Sectioning Request Form
class SectioningRequestForm(forms.ModelForm):
    special_request = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}), required=False, max_length=256)
    
    class Meta:
        model = SectioningRequest
        fields = ['requestor', 'study', 'special_request', 'assigned_to', 'cut_surface_down', 'sections_per_slide', 'slides_per_block', 'other', 'for_what', 'links']
        exclude = ['tissues']
        widgets = {
            'requestor': forms.Select(attrs={'class': 'form-control'}),
            'study': forms.Select(attrs={'class': 'form-control'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'cut_surface_down': forms.Select(attrs={'class': 'form-control'}, choices=[(True, 'Yes'), (False, 'No')]),
            'sections_per_slide': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'slides_per_block': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'other': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'maxlength': 256}),
            'for_what': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requestor'].queryset = Requestor.objects.all().order_by('name')
        self.fields['study'].queryset = Study.objects.all().order_by('study_id')
        self.fields['assigned_to'].queryset = Assignee.objects.all().order_by('name')
        self.fields['assigned_to'].required = False
        self.fields['sections_per_slide'].required = False
        self.fields['slides_per_block'].required = False
        self.fields['other'].required = False
        self.fields['for_what'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class EmbeddingRequestEditForm(forms.ModelForm):
    special_request = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}), required=False, max_length=256)
    
    class Meta:
        model = EmbeddingRequest
        fields = ['status', 'requestor', 'study', 'special_request', 'assigned_to', 'currently_in', 'take_down_date', 'length_of_time_in_etoh', 'number_of_animals', 'date_of_xylene_etoh_change']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'requestor': forms.Select(attrs={'class': 'form-control'}),
            'study': forms.Select(attrs={'class': 'form-control'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'currently_in': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Currently In'}),
            'take_down_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'length_of_time_in_etoh': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 40}),
            'number_of_animals': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Animals'}),
            'date_of_xylene_etoh_change': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all().order_by('status')
        self.fields['requestor'].queryset = Requestor.objects.all().order_by('name')
        self.fields['study'].queryset = Study.objects.all().order_by('study_id')
        self.fields['assigned_to'].queryset = Assignee.objects.all().order_by('name')
        self.fields['assigned_to'].required = False
        self.fields['currently_in'].required = False

class SectioningRequestEditForm(forms.ModelForm):
    special_request = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}), required=False, max_length=256)
    
    class Meta:
        model = SectioningRequest
        fields = ['status', 'requestor', 'study', 'special_request', 'assigned_to', 'cut_surface_down', 'sections_per_slide', 'slides_per_block', 'other', 'for_what']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'requestor': forms.Select(attrs={'class': 'form-control'}),
            'study': forms.Select(attrs={'class': 'form-control'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 256}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'cut_surface_down': forms.Select(attrs={'class': 'form-control'}, choices=[(True, 'Yes'), (False, 'No')]),
            'sections_per_slide': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'slides_per_block': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'other': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'maxlength': 256}),
            'for_what': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all().order_by('status')
        self.fields['requestor'].queryset = Requestor.objects.all().order_by('name')
        self.fields['study'].queryset = Study.objects.all().order_by('study_id')
        self.fields['assigned_to'].queryset = Assignee.objects.all().order_by('name')
        self.fields['assigned_to'].required = False
        self.fields['sections_per_slide'].required = False
        self.fields['slides_per_block'].required = False
        self.fields['other'].required = False
        self.fields['for_what'].required = False

# Staining Request Search Form
class StainingRequestSearchForm(forms.Form):
    request_id = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Request ID'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    requestor = forms.ModelChoiceField(queryset=Requestor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    antibody = forms.ModelChoiceField(queryset=Antibody.objects.filter(archived=False).order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    probe = forms.ModelChoiceField(queryset=Probe.objects.filter(archived=False).order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
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

# Sectioning Request Search Form
class SectioningRequestSearchForm(forms.Form):
    request_id = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Request ID'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    requestor = forms.ModelChoiceField(queryset=Requestor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    tissue = forms.ModelChoiceField(queryset=Tissue.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    study = forms.ModelChoiceField(queryset=Study.objects.all().order_by('study_id'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all().order_by('status'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    assigned_to = forms.ModelChoiceField(queryset=Assignee.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    special_request = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Special Request'}))
    cut_surface_down = forms.ChoiceField(choices=[('', 'All'), ('Yes', 'Yes'), ('No', 'No')], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    sections_per_slide = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sections per Slide'}))
    slides_per_block = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Slides per Block'}))
    other = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other'}))
    for_what = forms.ChoiceField(choices=[('', 'All'), ('H&E', 'H&E'), ('Special stain', 'Special stain'), ('IHC', 'IHC'), ('ISH', 'ISH'), ('other', 'Other')], required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add empty choice to all ModelChoiceFields
        self.fields['requestor'].empty_label = "Select Requestor"
        self.fields['tissue'].empty_label = "Select Tissue"
        self.fields['status'].empty_label = "Select Status"
        self.fields['assigned_to'].empty_label = "Select Assignee"

# Embedding Request Search Form
class EmbeddingRequestSearchForm(forms.Form):
    request_id = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Request ID'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    requestor = forms.ModelChoiceField(queryset=Requestor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    tissue = forms.ModelChoiceField(queryset=Tissue.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    study = forms.ModelChoiceField(queryset=Study.objects.all().order_by('study_id'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all().order_by('status'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    assigned_to = forms.ModelChoiceField(queryset=Assignee.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    special_request = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Special Request'}))
    number_of_animals = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Animals'}))
    take_down_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    currently_in = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Currently In'}))
    date_of_xylene_etoh_change = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    length_of_time_in_etoh = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Length of Time in EtOH'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add empty choice to all ModelChoiceFields
        self.fields['requestor'].empty_label = "Select Requestor"
        self.fields['tissue'].empty_label = "Select Tissue"
        self.fields['status'].empty_label = "Select Status"
        self.fields['assigned_to'].empty_label = "Select Assignee"

class StudyEditForm(forms.ModelForm):
    archived = forms.ChoiceField(
        choices=[(False, 'No'), (True, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=False,
        required=False
    )
    
    class Meta:
        model = Study
        fields = ['study_id', 'title', 'archived']
        widgets = {
            'study_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
        }

class AntibodyForm(forms.ModelForm):
    archived = forms.ChoiceField(
        choices=[(False, 'No'), (True, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=False,
        required=False
    )
    
    class Meta:
        model = Antibody
        fields = ['name', 'description', 'antigen', 'species', 'recognizes', 'vendor', 'archived']
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
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 256}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': 256}),
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
    archived = forms.ChoiceField(
        choices=[(False, 'No'), (True, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=False,
        required=False
    )
    
    class Meta:
        model = Probe
        fields = ['name', 'description', 'sequence', 'target_gene', 'vendor', 'catalog_number', 'platform', 'target_region', 'number_of_pairs', 'archived']
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


class BaseNotificationConfigForm(forms.Form):
    """Base form for configuring notification settings for different request statuses"""
    
    def __init__(self, request_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_type = request_type
        
        # Get all statuses
        statuses = Status.objects.all().order_by('status')
        
        # Create a checkbox field for each status
        for status in statuses:
            field_name = f'notify_{status.key}'
            self.fields[field_name] = forms.BooleanField(
                required=False,
                label=f'Notify when {request_type or "request"} status changes to "{status.status}"',
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )


class StainingNotificationConfigForm(BaseNotificationConfigForm):
    """Form for configuring staining request notifications"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(request_type="staining", *args, **kwargs)


class EmbeddingNotificationConfigForm(BaseNotificationConfigForm):
    """Form for configuring embedding request notifications"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(request_type="embedding", *args, **kwargs)


class SectioningNotificationConfigForm(BaseNotificationConfigForm):
    """Form for configuring sectioning request notifications"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(request_type="sectioning", *args, **kwargs)
