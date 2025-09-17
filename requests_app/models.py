from django.db import models
from django.utils import timezone
import json

# Create your models here.

PRIORITY_CHOICES = [
    (1, '1 - Low'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5 - High'),
]

class Requestor(models.Model):
    key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_display_fields(self):
        return [self.name]

class Status(models.Model):
    key = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100)
    status_set_at = models.DateTimeField(default=timezone.now, verbose_name="Status Set At")

    def __str__(self):
        return self.status

    def get_display_fields(self):
        return [self.status]

    @classmethod
    def get_default_status(cls):
        status, _ = cls.objects.get_or_create(status='Submitted')
        return status

class Assignee(models.Model):
    key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_display_fields(self):
        return [self.name, self.email, self.department]

class Priority(models.Model):
    key = models.AutoField(primary_key=True)
    value = models.IntegerField(unique=True)
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.value} - {self.label}"

    def get_display_fields(self):
        return [self.value, self.label, self.description]

    @classmethod
    def get_default_priority(cls):
        priority, _ = cls.objects.get_or_create(value=3, defaults={'label': '3 - Medium'})
        return priority

    @classmethod
    def initialize_defaults(cls):
        """Initialize default priority values if they don't exist"""
        defaults = [
            (1, '1 - Low', 'Low priority requests'),
            (2, '2', 'Low-medium priority'),
            (3, '3 - Medium', 'Medium priority requests'),
            (4, '4', 'Medium-high priority'),
            (5, '5 - High', 'High priority requests'),
        ]
        
        for value, label, description in defaults:
            cls.objects.get_or_create(
                value=value,
                defaults={'label': label, 'description': description}
            )

class Probe(models.Model):
    key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sequence = models.CharField(max_length=500, blank=True, null=True)
    target_gene = models.CharField(max_length=255, blank=True, null=True)
    vendor = models.CharField(max_length=255, blank=True, null=True)
    catalog_number = models.CharField(max_length=100, blank=True, null=True)
    platform = models.CharField(max_length=255, blank=True, null=True)
    target_region = models.CharField(max_length=255, blank=True, null=True)
    number_of_pairs = models.IntegerField(blank=True, null=True)
    archived = models.BooleanField(default=False, verbose_name="Archived")

    def __str__(self):
        return f"{self.name} - {self.description}"

    def get_name_only(self):
        return self.name

    def get_display_fields(self):
        return [self.name, self.description, self.sequence, self.target_gene, self.vendor, self.catalog_number, self.platform, self.target_region, self.number_of_pairs]

class Antibody(models.Model):
    key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    antigen = models.CharField(max_length=255)
    species = models.CharField(max_length=100)
    recognizes = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    archived = models.BooleanField(default=False, verbose_name="Archived")

    def __str__(self):
        return f"{self.name} - {self.description}"

    def get_name_only(self):
        return self.name

    def get_display_fields(self):
        return [self.name, self.description, self.antigen, self.species, self.recognizes, self.vendor]

class Study(models.Model):
    key = models.AutoField(primary_key=True)
    study_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    archived = models.BooleanField(default=False, verbose_name="Archived")

    def __str__(self):
        return f"{self.study_id} - {self.title}"

class Tissue(models.Model):
    key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_display_fields(self):
        return [self.name]

class Request(models.Model):
    key = models.AutoField(primary_key=True)
    data = models.JSONField()
    requestor = models.ForeignKey(Requestor, on_delete=models.CASCADE)
    antibody = models.ForeignKey(Antibody, on_delete=models.CASCADE)
    probe = models.ForeignKey(Probe, on_delete=models.CASCADE, null=True, blank=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)
    description = models.CharField(max_length=256, blank=True, null=True)
    special_request = models.TextField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=Status.get_default_status)
    notes = models.TextField(blank=True, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, default=3)
    assigned_to = models.ForeignKey(Assignee, on_delete=models.SET_NULL, null=True, blank=True)
    request_type = models.CharField(
        choices=[
            ("staining", "Staining Request"),
            ("embedding", "Embedding Request"),
            ("sectioning", "Sectioning Request"),
        ],
        default="staining",
        max_length=20,
    )
    status_timestamp = models.DateTimeField(default=timezone.now, verbose_name="Status Set At")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.key} - {self.antibody.name}"

# Staining Request Model (using existing Request model for now)
class StainingRequest(Request):
    class Meta:
        proxy = True
        verbose_name = "Staining Request"
        verbose_name_plural = "Staining Requests"

    def __str__(self):
        return f"Staining Request {self.key} - {self.antibody.name}"

# Embedding Request Model (existing model)
class EmbeddingRequest(models.Model):
    key = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    special_request = models.TextField(blank=True, null=True)
    number_of_animals = models.IntegerField(blank=True, null=True, verbose_name="Number of Animals")
    take_down_date = models.DateField(blank=True, null=True, verbose_name="Take Down Date")
    currently_in = models.BooleanField(choices=[(True, "Yes"), (False, "No")], default=False, verbose_name="Currently In?")
    date_of_xylene_etoh_change = models.DateField(blank=True, null=True, verbose_name="Date of Xylene-EtOH Change")
    length_of_time_in_etoh = models.CharField(blank=True, max_length=40, null=True, verbose_name="Length of Time in EtOH")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_timestamp = models.DateTimeField(default=timezone.now, verbose_name="Status Set At")
    
    # Foreign Keys
    assigned_to = models.ForeignKey(Assignee, blank=True, null=True, on_delete=models.SET_NULL)
    requestor = models.ForeignKey(Requestor, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, default=Status.get_default_status, on_delete=models.CASCADE)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    tissues = models.ManyToManyField(Tissue, blank=True)
    
    class Meta:
        verbose_name = "Embedding Request"
        verbose_name_plural = "Embedding Requests"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Embedding Request {self.key} - {self.requestor.name}"

# Sectioning Request Model (existing model)
class SectioningRequest(models.Model):
    key = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    special_request = models.TextField(blank=True, null=True)
    cut_surface_down = models.BooleanField(default=False, verbose_name="Cut Surface Down")
    other = models.TextField(blank=True, null=True, verbose_name="Other")
    sections_per_slide = models.IntegerField(blank=True, null=True, verbose_name="# of Sections/Slide")
    slides_per_block = models.IntegerField(blank=True, null=True, verbose_name="# of Slides/Block")
    for_what = models.CharField(choices=[("H&E", "H&E"), ("Special stain", "Special stain"), ("IHC", "IHC"), ("ISH", "ISH"), ("other", "Other")], default="H&E", max_length=20, verbose_name="For")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_timestamp = models.DateTimeField(default=timezone.now, verbose_name="Status Set At")
    
    # Foreign Keys
    assigned_to = models.ForeignKey(Assignee, blank=True, null=True, on_delete=models.SET_NULL)
    requestor = models.ForeignKey(Requestor, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, default=Status.get_default_status, on_delete=models.CASCADE)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    tissues = models.ManyToManyField(Tissue, blank=True)
    
    class Meta:
        verbose_name = "Sectioning Request"
        verbose_name_plural = "Sectioning Requests"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Sectioning Request {self.key} - {self.requestor.name}"


# Change Log Models
class BaseChangeLog(models.Model):
    """Base model for all change logs"""
    change_type = models.CharField(
        choices=[
            ('created', 'Created'),
            ('updated', 'Updated'),
            ('deleted', 'Deleted'),
        ],
        max_length=20
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(blank=True, max_length=256, null=True)
    changed_fields = models.JSONField(blank=True, default=list)
    change_summary = models.TextField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)  # Store the complete request data at time of change
    
    class Meta:
        abstract = True
        ordering = ['-changed_at']


class StainingRequestChangeLog(BaseChangeLog):
    """Change log for StainingRequest"""
    request = models.ForeignKey(StainingRequest, on_delete=models.CASCADE, related_name='change_logs')
    requestor = models.ForeignKey(Requestor, blank=True, null=True, on_delete=models.SET_NULL)
    study = models.ForeignKey(Study, blank=True, null=True, on_delete=models.SET_NULL)
    tissue = models.ForeignKey(Tissue, blank=True, null=True, on_delete=models.SET_NULL)
    antibody = models.ForeignKey(Antibody, blank=True, null=True, on_delete=models.SET_NULL)
    probe = models.ForeignKey(Probe, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(Assignee, blank=True, null=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(Priority, blank=True, null=True, on_delete=models.SET_NULL)
    special_request = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Staining Request Change Log"
        verbose_name_plural = "Staining Request Change Logs"
        ordering = ['-changed_at']
    
    @classmethod
    def get_request_history(cls, request_id):
        """Get all versions of a request ordered by change time"""
        return cls.objects.filter(request_id=request_id).order_by('changed_at')
    
    @classmethod
    def log_change(cls, request, change_type, changed_fields=None, description=None):
        """Log a change to a StainingRequest"""
        # Store current state of the request
        data = {
            'requestor': request.requestor.key if request.requestor else None,
            'study': request.study.key if request.study else None,
            'tissue': request.tissue.key if request.tissue else None,
            'antibody': request.antibody.key if request.antibody else None,
            'probe': request.probe.key if request.probe else None,
            'status': request.status.key if request.status else None,
            'assigned_to': request.assigned_to.key if request.assigned_to else None,
            'priority': request.priority.key if request.priority else None,
            'special_request': request.special_request,
            'notes': request.notes,
        }
        
        return cls.objects.create(
            request=request,
            change_type=change_type,
            description=description,
            changed_fields=changed_fields or [],
            data=data,
            requestor=request.requestor,
            study=request.study,
            tissue=request.tissue,
            antibody=request.antibody,
            probe=request.probe,
            status=request.status,
            assigned_to=request.assigned_to,
            priority=request.priority,
            special_request=request.special_request,
            notes=request.notes,
        )


class EmbeddingRequestChangeLog(BaseChangeLog):
    """Change log for EmbeddingRequest"""
    request = models.ForeignKey(EmbeddingRequest, on_delete=models.CASCADE, related_name='change_logs')
    requestor = models.ForeignKey(Requestor, blank=True, null=True, on_delete=models.SET_NULL)
    study = models.ForeignKey(Study, blank=True, null=True, on_delete=models.SET_NULL)
    tissues = models.ManyToManyField(Tissue, blank=True)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(Assignee, blank=True, null=True, on_delete=models.SET_NULL)
    special_request = models.TextField(blank=True, null=True)
    number_of_animals = models.IntegerField(blank=True, null=True)
    take_down_date = models.DateField(blank=True, null=True)
    currently_in = models.BooleanField(blank=True, null=True)
    date_of_xylene_etoh_change = models.DateField(blank=True, null=True)
    length_of_time_in_etoh = models.CharField(blank=True, max_length=40, null=True)
    
    class Meta:
        verbose_name = "Embedding Request Change Log"
        verbose_name_plural = "Embedding Request Change Logs"
        ordering = ['-changed_at']
    
    @classmethod
    def get_request_history(cls, request_id):
        """Get all versions of a request ordered by change time"""
        return cls.objects.filter(request_id=request_id).order_by('changed_at')
    
    @classmethod
    def log_change(cls, request, change_type, changed_fields=None, description=None):
        """Log a change to an EmbeddingRequest"""
        # Store current state of the request
        data = {
            'requestor': request.requestor.key if request.requestor else None,
            'study': request.study.key if request.study else None,
            'tissues': [t.key for t in request.tissues.all()],
            'status': request.status.key if request.status else None,
            'assigned_to': request.assigned_to.key if request.assigned_to else None,
            'special_request': request.special_request,
            'number_of_animals': request.number_of_animals,
            'take_down_date': request.take_down_date.isoformat() if request.take_down_date else None,
            'currently_in': request.currently_in,
            'date_of_xylene_etoh_change': request.date_of_xylene_etoh_change.isoformat() if request.date_of_xylene_etoh_change else None,
            'length_of_time_in_etoh': request.length_of_time_in_etoh,
        }
        
        return cls.objects.create(
            request=request,
            change_type=change_type,
            description=description,
            changed_fields=changed_fields or [],
            data=data,
            requestor=request.requestor,
            study=request.study,
            tissues=request.tissues,
            status=request.status,
            assigned_to=request.assigned_to,
            special_request=request.special_request,
            number_of_animals=request.number_of_animals,
            take_down_date=request.take_down_date,
            currently_in=request.currently_in,
            date_of_xylene_etoh_change=request.date_of_xylene_etoh_change,
            length_of_time_in_etoh=request.length_of_time_in_etoh,
        )


class SectioningRequestChangeLog(BaseChangeLog):
    """Change log for SectioningRequest"""
    request = models.ForeignKey(SectioningRequest, on_delete=models.CASCADE, related_name='change_logs')
    requestor = models.ForeignKey(Requestor, blank=True, null=True, on_delete=models.SET_NULL)
    study = models.ForeignKey(Study, blank=True, null=True, on_delete=models.SET_NULL)
    tissues = models.ManyToManyField(Tissue, blank=True)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(Assignee, blank=True, null=True, on_delete=models.SET_NULL)
    special_request = models.TextField(blank=True, null=True)
    cut_surface_down = models.BooleanField(blank=True, null=True)
    sections_per_slide = models.IntegerField(blank=True, null=True)
    slides_per_block = models.IntegerField(blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    for_what = models.CharField(blank=True, max_length=20, null=True)
    
    class Meta:
        verbose_name = "Sectioning Request Change Log"
        verbose_name_plural = "Sectioning Request Change Logs"
        ordering = ['-changed_at']
    
    @classmethod
    def get_request_history(cls, request_id):
        """Get all versions of a request ordered by change time"""
        return cls.objects.filter(request_id=request_id).order_by('changed_at')
    
    @classmethod
    def log_change(cls, request, change_type, changed_fields=None, description=None):
        """Log a change to a SectioningRequest"""
        # Store current state of the request
        data = {
            'requestor': request.requestor.key if request.requestor else None,
            'study': request.study.key if request.study else None,
            'tissues': [t.key for t in request.tissues.all()],
            'status': request.status.key if request.status else None,
            'assigned_to': request.assigned_to.key if request.assigned_to else None,
            'special_request': request.special_request,
            'cut_surface_down': request.cut_surface_down,
            'sections_per_slide': request.sections_per_slide,
            'slides_per_block': request.slides_per_block,
            'other': request.other,
            'for_what': request.for_what,
        }
        
        return cls.objects.create(
            request=request,
            change_type=change_type,
            description=description,
            changed_fields=changed_fields or [],
            data=data,
            requestor=request.requestor,
            study=request.study,
            tissues=request.tissues,
            status=request.status,
            assigned_to=request.assigned_to,
            special_request=request.special_request,
            cut_surface_down=request.cut_surface_down,
            sections_per_slide=request.sections_per_slide,
            slides_per_block=request.slides_per_block,
            other=request.other,
            for_what=request.for_what,
        )
