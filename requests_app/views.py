from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import RequestForm, RequestEditForm, RequestSearchForm, StudyEditForm
from .models import Request, Status, Study, Requestor, Antibody, Tissue
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
import re

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
        
        # Populate the data JSONField with form data
        request_obj.data = {
            'date': self.request.POST.get('date'),
            'description': form.cleaned_data.get('description'),
            'special_request': form.cleaned_data.get('special_request'),
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
    fields = ['title']
    template_name = 'requests_app/study_edit.html'
    success_url = reverse_lazy('study_list')

class StudyListView(ListView):
    model = Study
    template_name = 'requests_app/study_list.html'
    context_object_name = 'studies'

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

class RequestorUpdateView(UpdateView):
    model = Requestor
    fields = ['name']
    template_name = 'requests_app/requestor_edit.html'
    success_url = reverse_lazy('requestor_list')

def sanitize_input(input_str):
    # Remove HTML tags
    input_str = re.sub(r'<[^>]*>', '', input_str)
    # Remove script tags
    input_str = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', input_str, flags=re.IGNORECASE)
    # Remove potentially dangerous characters
    input_str = re.sub(r'[&<>"\']', '', input_str)
    return input_str

def validate_input(input_str):
    if not input_str or len(input_str.strip()) == 0:
        return False
    if len(input_str) > 256:
        return False
    return True

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

class AntibodyUpdateView(UpdateView):
    model = Antibody
    fields = ['name', 'description', 'antigen', 'species', 'recognizes', 'vendor']
    template_name = 'requests_app/antibody_edit.html'
    success_url = reverse_lazy('antibody_list')

def antibody_create(request):
    if request.method == 'POST':
        name = sanitize_input(request.POST.get('name', '').strip())
        description = sanitize_input(request.POST.get('description', '').strip())
        antigen = sanitize_input(request.POST.get('antigen', '').strip())
        species = sanitize_input(request.POST.get('species', '').strip())
        recognizes = sanitize_input(request.POST.get('recognizes', '').strip())
        vendor = sanitize_input(request.POST.get('vendor', '').strip())
        
        if all(validate_input(field) for field in [name, description, antigen, species, recognizes, vendor]):
            Antibody.objects.create(
                name=name,
                description=description,
                antigen=antigen,
                species=species,
                recognizes=recognizes,
                vendor=vendor
            )
            return redirect('antibody_list')
        else:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    return render(request, 'requests_app/antibody_form.html', {'title': 'Add New Antibody'})

# Tissue Views
class TissueListView(ListView):
    model = Tissue
    template_name = 'requests_app/tissue_list.html'
    context_object_name = 'tissues'

class TissueUpdateView(UpdateView):
    model = Tissue
    fields = ['name']
    template_name = 'requests_app/tissue_edit.html'
    success_url = reverse_lazy('tissue_list')

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

class StatusUpdateView(UpdateView):
    model = Status
    fields = ['status']
    template_name = 'requests_app/status_edit.html'
    success_url = reverse_lazy('status_list')
