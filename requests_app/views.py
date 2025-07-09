from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .forms import RequestForm, RequestEditForm, RequestSearchForm, StudyEditForm, AntibodyForm, RequestorForm, TissueForm, StatusForm
from .models import Request, Status, Study, Requestor, Antibody, Tissue
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
import re
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import openpyxl
import os

# Create your views here.

def home(request):
    return render(request, 'requests_app/home.html')

def data_management(request):
    return render(request, 'requests_app/data_management.html')

# Request Views
class RequestListView(ListView):
    model = Request
    template_name = 'requests_app/request_list.html'
    context_object_name = 'requests'
    paginate_by = 20

    def get_queryset(self):
        queryset = Request.objects.all()
        
        # Get sort parameters
        sort_by = self.request.GET.get('sort', '-created_at')
        order = self.request.GET.get('order', 'desc')
        
        # Validate sort field to prevent injection
        allowed_fields = ['key', 'created_at', 'requestor__name', 'description', 'antibody__name', 'study__title', 'tissue__name', 'status__status']
        if sort_by.lstrip('-') not in [field.lstrip('-') for field in allowed_fields]:
            sort_by = '-created_at'
        
        # Apply sorting
        if order == 'asc' and sort_by.startswith('-'):
            sort_by = sort_by[1:]
        elif order == 'desc' and not sort_by.startswith('-'):
            sort_by = '-' + sort_by
            
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        context['current_order'] = self.request.GET.get('order', 'desc')
        return context

class RequestDetailView(DetailView):
    model = Request
    template_name = 'requests_app/request_detail.html'
    context_object_name = 'request'

class RequestCreateView(FormView):
    template_name = 'requests_app/request_form.html'
    form_class = RequestForm
    success_url = reverse_lazy('request_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today_date'] = datetime.now().date()
        context['tissues'] = Tissue.objects.all()
        context['max_tissues'] = 10
        return context

    def form_valid(self, form):
        request_obj = form.save(commit=False)
        request_obj.status = Status.get_default_status()
        
        # Collect additional tissues from form data
        additional_tissues = []
        for key, value in self.request.POST.items():
            if key.startswith('tissue_') and value:  # tissue_0, tissue_1, etc.
                try:
                    tissue_id = int(value)
                    tissue = Tissue.objects.get(pk=tissue_id)
                    additional_tissues.append(tissue.name)
                except (ValueError, Tissue.DoesNotExist):
                    pass
        
        # Populate the data JSONField with form data
        request_obj.data = {
            'date': self.request.POST.get('date'),
            'description': form.cleaned_data.get('description'),
            'special_request': form.cleaned_data.get('special_request'),
            'tissues': additional_tissues,
        }
        
        request_obj.save()
        return super().form_valid(form)

class RequestUpdateView(UpdateView):
    model = Request
    form_class = RequestEditForm
    template_name = 'requests_app/request_edit.html'
    success_url = reverse_lazy('request_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request_obj'] = self.object
        context['antibodies'] = Antibody.objects.all()
        context['studies'] = Study.objects.all()
        context['tissues'] = Tissue.objects.all()
        context['statuses'] = Status.objects.all()
        return context

class RequestDeleteView(DeleteView):
    model = Request
    template_name = 'requests_app/request_confirm_delete.html'
    success_url = reverse_lazy('request_list')
    context_object_name = 'request'

class RequestSearchView(ListView):
    model = Request
    template_name = 'requests_app/request_search.html'
    context_object_name = 'requests'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RequestSearchForm(self.request.GET)
        context['tissues'] = Tissue.objects.all()
        return context

    def get_queryset(self):
        queryset = Request.objects.all()
        form = RequestSearchForm(self.request.GET)
        
        if form.is_valid():
            request_id = form.cleaned_data.get('request_id')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            requestor = form.cleaned_data.get('requestor')
            tissue = form.cleaned_data.get('tissue')
            study = form.cleaned_data.get('study')

            if request_id:
                queryset = queryset.filter(key=request_id)
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
            if requestor:
                queryset = queryset.filter(requestor=requestor)
            if tissue:
                queryset = queryset.filter(tissue__name__icontains=tissue)
            if study:
                queryset = queryset.filter(study=study)

        return queryset.order_by('-created_at')

# Study Views
class StudyUpdateView(UpdateView):
    model = Study
    form_class = StudyEditForm
    template_name = 'requests_app/study_edit.html'
    success_url = reverse_lazy('study_list')

class StudyListView(ListView):
    model = Study
    template_name = 'requests_app/study_list.html'
    context_object_name = 'studies'

    def get_queryset(self):
        queryset = Study.objects.all()
        
        # Get sort parameters
        sort_by = self.request.GET.get('sort', 'key')
        order = self.request.GET.get('order', 'asc')
        
        # Validate sort field to prevent injection
        allowed_fields = ['key', 'study_id', 'title']
        if sort_by.lstrip('-') not in [field.lstrip('-') for field in allowed_fields]:
            sort_by = 'key'
        
        # Apply sorting
        if order == 'asc' and sort_by.startswith('-'):
            sort_by = sort_by[1:]
        elif order == 'desc' and not sort_by.startswith('-'):
            sort_by = '-' + sort_by
            
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'key')
        context['current_order'] = self.request.GET.get('order', 'asc')
        return context

class StudyDeleteView(DeleteView):
    model = Study
    template_name = 'requests_app/study_confirm_delete.html'
    success_url = reverse_lazy('study_list')
    context_object_name = 'study'

def study_create(request):
    if request.method == 'POST':
        study_id = request.POST.get('study_id', '').strip()
        title = request.POST.get('title', '').strip()
        
        study_id = sanitize_input(study_id)
        title = sanitize_input(title)
        
        if validate_input(study_id) and validate_input(title):
            Study.objects.create(study_id=study_id, title=title)
            return redirect('study_list')
        else:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    
    return render(request, 'requests_app/study_form.html', {'title': 'Add New Study'})

# Requestor Views
class RequestorListView(ListView):
    model = Requestor
    template_name = 'requests_app/requestor_list.html'
    context_object_name = 'requestors'

    def get_queryset(self):
        queryset = Requestor.objects.all()
        
        # Get sort parameters
        sort_by = self.request.GET.get('sort', 'key')
        order = self.request.GET.get('order', 'asc')
        
        # Validate sort field to prevent injection
        allowed_fields = ['key', 'name']
        if sort_by.lstrip('-') not in [field.lstrip('-') for field in allowed_fields]:
            sort_by = 'key'
        
        # Apply sorting
        if order == 'asc' and sort_by.startswith('-'):
            sort_by = sort_by[1:]
        elif order == 'desc' and not sort_by.startswith('-'):
            sort_by = '-' + sort_by
            
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'key')
        context['current_order'] = self.request.GET.get('order', 'asc')
        return context

class RequestorUpdateView(UpdateView):
    model = Requestor
    form_class = RequestorForm
    template_name = 'requests_app/requestor_edit.html'
    success_url = reverse_lazy('requestor_list')

class RequestorDeleteView(DeleteView):
    model = Requestor
    template_name = 'requests_app/requestor_confirm_delete.html'
    success_url = reverse_lazy('requestor_list')
    context_object_name = 'requestor'

def sanitize_input(input_str):
    # Remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', input_str)

def validate_input(input_str):
    # Check if input is not empty and contains only allowed characters
    if not input_str or len(input_str) > 256:
        return False
    # Allow letters, numbers, spaces, hyphens, and underscores
    return bool(re.match(r'^[a-zA-Z0-9\s\-_]+$', input_str))

def validate_import_input(input_str):
    # More permissive validation for imports - allows common characters in study titles and IDs
    if not input_str or len(input_str) > 256:
        return False
    # Allow letters, numbers, spaces, hyphens, underscores, parentheses, colons, periods, and commas
    return bool(re.match(r'^[a-zA-Z0-9\s\-_\(\):.,]+$', input_str))

def requestor_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        name = sanitize_input(name)
        
        if validate_input(name):
            Requestor.objects.create(name=name)
            return redirect('requestor_list')
        else:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    
    return render(request, 'requests_app/requestor_form.html', {'title': 'Add New Requestor'})

# Antibody Views
class AntibodyListView(ListView):
    model = Antibody
    template_name = 'requests_app/antibody_list.html'
    context_object_name = 'antibodies'

    def get_queryset(self):
        queryset = Antibody.objects.all()
        
        # Get sort parameters
        sort_by = self.request.GET.get('sort', 'key')
        order = self.request.GET.get('order', 'asc')
        
        # Validate sort field to prevent injection
        allowed_fields = ['key', 'name', 'description', 'antigen', 'species', 'recognizes', 'vendor']
        if sort_by.lstrip('-') not in [field.lstrip('-') for field in allowed_fields]:
            sort_by = 'key'
        
        # Apply sorting
        if order == 'asc' and sort_by.startswith('-'):
            sort_by = sort_by[1:]
        elif order == 'desc' and not sort_by.startswith('-'):
            sort_by = '-' + sort_by
            
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'key')
        context['current_order'] = self.request.GET.get('order', 'asc')
        return context

class AntibodyUpdateView(UpdateView):
    model = Antibody
    form_class = AntibodyForm
    template_name = 'requests_app/antibody_edit.html'
    success_url = reverse_lazy('antibody_list')

class AntibodyDeleteView(DeleteView):
    model = Antibody
    template_name = 'requests_app/antibody_confirm_delete.html'
    success_url = reverse_lazy('antibody_list')
    context_object_name = 'antibody'

def antibody_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        antigen = request.POST.get('antigen', '').strip()
        species = request.POST.get('species', '').strip()
        recognizes = request.POST.get('recognizes', '').strip()
        vendor = request.POST.get('vendor', '').strip()
        
        name = sanitize_input(name)
        description = sanitize_input(description)
        antigen = sanitize_input(antigen)
        species = sanitize_input(species)
        recognizes = sanitize_input(recognizes)
        vendor = sanitize_input(vendor)
        
        if validate_input(name) and validate_input(description) and validate_input(antigen) and validate_input(species) and validate_input(recognizes) and validate_input(vendor):
            Antibody.objects.create(name=name, description=description, antigen=antigen, species=species, recognizes=recognizes, vendor=vendor)
            return redirect('antibody_list')
        else:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    
    return render(request, 'requests_app/antibody_form.html', {'title': 'Add New Antibody'})

# Tissue Views
class TissueListView(ListView):
    model = Tissue
    template_name = 'requests_app/tissue_list.html'
    context_object_name = 'tissues'

    def get_queryset(self):
        queryset = Tissue.objects.all()
        
        # Get sort parameters
        sort_by = self.request.GET.get('sort', 'key')
        order = self.request.GET.get('order', 'asc')
        
        # Validate sort field to prevent injection
        allowed_fields = ['key', 'name']
        if sort_by.lstrip('-') not in [field.lstrip('-') for field in allowed_fields]:
            sort_by = 'key'
        
        # Apply sorting
        if order == 'asc' and sort_by.startswith('-'):
            sort_by = sort_by[1:]
        elif order == 'desc' and not sort_by.startswith('-'):
            sort_by = '-' + sort_by
            
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'key')
        context['current_order'] = self.request.GET.get('order', 'asc')
        return context

class TissueUpdateView(UpdateView):
    model = Tissue
    form_class = TissueForm
    template_name = 'requests_app/tissue_edit.html'
    success_url = reverse_lazy('tissue_list')

class TissueDeleteView(DeleteView):
    model = Tissue
    template_name = 'requests_app/tissue_confirm_delete.html'
    success_url = reverse_lazy('tissue_list')
    context_object_name = 'tissue'

def tissue_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        name = sanitize_input(name)
        
        if validate_input(name):
            Tissue.objects.create(name=name)
            return redirect('tissue_list')
        else:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    
    return render(request, 'requests_app/tissue_form.html', {'title': 'Add New Tissue'})

# Status Views
class StatusListView(ListView):
    model = Status
    template_name = 'requests_app/status_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        queryset = Status.objects.all()
        
        # Get sort parameters
        sort_by = self.request.GET.get('sort', 'key')
        order = self.request.GET.get('order', 'asc')
        
        # Validate sort field to prevent injection
        allowed_fields = ['key', 'status']
        if sort_by.lstrip('-') not in [field.lstrip('-') for field in allowed_fields]:
            sort_by = 'key'
        
        # Apply sorting
        if order == 'asc' and sort_by.startswith('-'):
            sort_by = sort_by[1:]
        elif order == 'desc' and not sort_by.startswith('-'):
            sort_by = '-' + sort_by
            
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'key')
        context['current_order'] = self.request.GET.get('order', 'asc')
        return context

class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'requests_app/status_edit.html'
    success_url = reverse_lazy('status_list')

class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'requests_app/status_confirm_delete.html'
    success_url = reverse_lazy('status_list')
    context_object_name = 'status'

def status_create(request):
    if request.method == 'POST':
        status = request.POST.get('status', '').strip()
        
        status = sanitize_input(status)
        
        if validate_input(status):
            Status.objects.create(status=status)
            return redirect('status_list')
        else:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    
    return render(request, 'requests_app/status_form.html', {'title': 'Add New Status'})

def custom_404(request, exception):
    return render(request, "404.html", status=404)

def custom_500(request):
    return render(request, "500.html", status=500)

def import_studies_from_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'No file was uploaded.')
            return redirect('study_list')
        
        uploaded_file = request.FILES['file']
        
        # Check file extension
        if not uploaded_file.name.endswith('.xlsx'):
            messages.error(request, 'Please upload an Excel file (.xlsx)')
            return redirect('study_list')
        
        try:
            # Read the Excel file
            workbook = openpyxl.load_workbook(uploaded_file)
            sheet = workbook.active
            
            # Check if the first row contains the expected headers
            first_row = [cell.value for cell in sheet[1]]
            if len(first_row) < 2:
                messages.error(request, 'File formatting is incorrect for study')
                return redirect('study_list')
            
            # Check for required headers (case insensitive)
            first_row_lower = [str(cell).lower().strip() if cell else '' for cell in first_row]
            study_id_index = None
            title_index = None
            
            for i, header in enumerate(first_row_lower):
                if 'study id' in header:
                    study_id_index = i
                elif 'title' in header:
                    title_index = i
            
            if study_id_index is None or title_index is None:
                messages.error(request, 'File formatting is incorrect for study')
                return redirect('study_list')
            
            # Process each row starting from the second row
            imported_count = 0
            for row_num in range(2, sheet.max_row + 1):
                study_id_cell = sheet.cell(row=row_num, column=study_id_index + 1)
                title_cell = sheet.cell(row=row_num, column=title_index + 1)
                
                study_id = study_id_cell.value
                title = title_cell.value
                
                # Skip empty rows
                if not study_id or not title:
                    continue
                
                # Clean and validate the data
                study_id = str(study_id).strip()
                title = str(title).strip()
                
                if validate_import_input(study_id) and validate_import_input(title):
                    # Check if study already exists
                    if not Study.objects.filter(study_id=study_id).exists():
                        Study.objects.create(study_id=study_id, title=title)
                        imported_count += 1
            
            if imported_count > 0:
                messages.success(request, f'Successfully imported {imported_count} studies.')
            else:
                messages.warning(request, 'No new studies were imported.')
                
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
        
        return redirect('study_list')
    
    return redirect('study_list')

def import_antibodies_from_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'No file was uploaded.')
            return redirect('antibody_list')
        
        uploaded_file = request.FILES['file']
        
        # Check file extension
        if not uploaded_file.name.endswith('.xlsx'):
            messages.error(request, 'Please upload an Excel file (.xlsx)')
            return redirect('antibody_list')
        
        try:
            # Read the Excel file
            workbook = openpyxl.load_workbook(uploaded_file)
            sheet = workbook.active
            
            # Check if the first row contains the expected headers
            first_row = [cell.value for cell in sheet[1]]
            if len(first_row) < 6:
                messages.error(request, 'File formatting is incorrect for antibody')
                return redirect('antibody_list')
            
            # Check for required headers (case insensitive)
            first_row_lower = [str(cell).lower().strip() if cell else '' for cell in first_row]
            name_index = None
            description_index = None
            antigen_index = None
            species_index = None
            recognizes_index = None
            vendor_index = None
            
            for i, header in enumerate(first_row_lower):
                if 'name' in header:
                    name_index = i
                elif 'description' in header:
                    description_index = i
                elif 'antigen' in header:
                    antigen_index = i
                elif 'species' in header:
                    species_index = i
                elif 'recognizes' in header:
                    recognizes_index = i
                elif 'vendor' in header:
                    vendor_index = i
            
            if (name_index is None or description_index is None or antigen_index is None or 
                species_index is None or recognizes_index is None or vendor_index is None):
                messages.error(request, 'File formatting is incorrect for antibody')
                return redirect('antibody_list')
            
            # Process each row starting from the second row
            imported_count = 0
            for row_num in range(2, sheet.max_row + 1):
                name_cell = sheet.cell(row=row_num, column=name_index + 1)
                description_cell = sheet.cell(row=row_num, column=description_index + 1)
                antigen_cell = sheet.cell(row=row_num, column=antigen_index + 1)
                species_cell = sheet.cell(row=row_num, column=species_index + 1)
                recognizes_cell = sheet.cell(row=row_num, column=recognizes_index + 1)
                vendor_cell = sheet.cell(row=row_num, column=vendor_index + 1)
                
                name = name_cell.value
                description = description_cell.value
                antigen = antigen_cell.value
                species = species_cell.value
                recognizes = recognizes_cell.value
                vendor = vendor_cell.value
                
                # Skip empty rows (name is required)
                if not name:
                    continue
                
                # Clean and validate the data
                name = str(name).strip()
                description = str(description).strip() if description else ''
                antigen = str(antigen).strip() if antigen else ''
                species = str(species).strip() if species else ''
                recognizes = str(recognizes).strip() if recognizes else ''
                vendor = str(vendor).strip() if vendor else ''
                
                if validate_import_input(name):
                    # Check if antibody already exists
                    if not Antibody.objects.filter(name=name).exists():
                        Antibody.objects.create(
                            name=name,
                            description=description,
                            antigen=antigen,
                            species=species,
                            recognizes=recognizes,
                            vendor=vendor
                        )
                        imported_count += 1
            
            if imported_count > 0:
                messages.success(request, f'Successfully imported {imported_count} antibodies.')
            else:
                messages.warning(request, 'No new antibodies were imported.')
                
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
        
        return redirect('antibody_list')
    
    return redirect('antibody_list')
