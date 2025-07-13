from django.db import models

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

    def __str__(self):
        return self.status

    def get_display_fields(self):
        return [self.status]

    @classmethod
    def get_default_status(cls):
        status, _ = cls.objects.get_or_create(status='submitted')
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.key} - {self.antibody.name}"
