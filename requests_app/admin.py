from django.contrib import admin
from .models import Requestor, Antibody, Study, Tissue, Request, Status, Assignee, Probe, Priority, EmbeddingRequest, SectioningRequest, StainingRequestChangeLog, EmbeddingRequestChangeLog, SectioningRequestChangeLog
from .forms import AntibodyForm, ProbeForm, StudyEditForm

# Register your models here.
admin.site.register(Requestor)
admin.site.register(Tissue)
admin.site.register(Request)
admin.site.register(Status)
admin.site.register(Assignee)
admin.site.register(Priority)
admin.site.register(EmbeddingRequest)
admin.site.register(SectioningRequest)

# Custom admin for models with archived field
@admin.register(Antibody)
class AntibodyAdmin(admin.ModelAdmin):
    form = AntibodyForm
    list_display = ('name', 'description', 'antigen', 'species', 'vendor', 'archived')
    list_filter = ('archived', 'species', 'vendor')
    search_fields = ('name', 'description', 'antigen', 'species', 'vendor')
    list_editable = ('archived',)

@admin.register(Probe)
class ProbeAdmin(admin.ModelAdmin):
    form = ProbeForm
    list_display = ('name', 'description', 'target_gene', 'vendor', 'platform', 'archived')
    list_filter = ('archived', 'platform', 'vendor')
    search_fields = ('name', 'description', 'target_gene', 'vendor', 'platform')
    list_editable = ('archived',)

@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    form = StudyEditForm
    list_display = ('study_id', 'title', 'archived')
    list_filter = ('archived',)
    search_fields = ('study_id', 'title')
    list_editable = ('archived',)

# Custom admin for change log models
@admin.register(StainingRequestChangeLog)
class StainingRequestChangeLogAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'requestor', 'status', 'change_type', 'changed_at', 'description')
    list_filter = ('change_type', 'status', 'changed_at', 'requestor')
    search_fields = ('request__key', 'requestor__name', 'status__status', 'description')
    readonly_fields = ('request', 'requestor', 'study', 'tissue', 'antibody', 'probe', 'status', 'assigned_to', 'priority', 'special_request', 'notes', 'change_type', 'changed_at', 'description', 'changed_fields', 'change_summary', 'data')
    ordering = ('-changed_at',)
    list_per_page = 50
    
    def request_id(self, obj):
        return f"#{obj.request.key}"
    request_id.short_description = 'Request ID'
    request_id.admin_order_field = 'request__key'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(EmbeddingRequestChangeLog)
class EmbeddingRequestChangeLogAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'requestor', 'status', 'change_type', 'changed_at', 'description')
    list_filter = ('change_type', 'status', 'changed_at', 'requestor')
    search_fields = ('request__key', 'requestor__name', 'status__status', 'description')
    readonly_fields = ('request', 'requestor', 'study', 'tissues', 'status', 'assigned_to', 'special_request', 'number_of_animals', 'take_down_date', 'currently_in', 'date_of_xylene_etoh_change', 'length_of_time_in_etoh', 'change_type', 'changed_at', 'description', 'changed_fields', 'change_summary', 'data')
    ordering = ('-changed_at',)
    list_per_page = 50
    
    def request_id(self, obj):
        return f"#{obj.request.key}"
    request_id.short_description = 'Request ID'
    request_id.admin_order_field = 'request__key'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SectioningRequestChangeLog)
class SectioningRequestChangeLogAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'requestor', 'status', 'change_type', 'changed_at', 'description')
    list_filter = ('change_type', 'status', 'changed_at', 'requestor')
    search_fields = ('request__key', 'requestor__name', 'status__status', 'description')
    readonly_fields = ('request', 'requestor', 'study', 'tissues', 'status', 'assigned_to', 'special_request', 'cut_surface_down', 'sections_per_slide', 'slides_per_block', 'other', 'for_what', 'change_type', 'changed_at', 'description', 'changed_fields', 'change_summary', 'data')
    ordering = ('-changed_at',)
    list_per_page = 50
    
    def request_id(self, obj):
        return f"#{obj.request.key}"
    request_id.short_description = 'Request ID'
    request_id.admin_order_field = 'request__key'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
