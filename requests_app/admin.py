from django.contrib import admin
from .models import Requestor, Antibody, Study, Tissue, Request, Status, Assignee, Probe, Priority, EmbeddingRequest, SectioningRequest, StainingRequestChangeLog, EmbeddingRequestChangeLog, SectioningRequestChangeLog

# Register your models here.
admin.site.register(Requestor)
admin.site.register(Antibody)
admin.site.register(Study)
admin.site.register(Tissue)
admin.site.register(Request)
admin.site.register(Status)
admin.site.register(Assignee)
admin.site.register(Probe)
admin.site.register(Priority)
admin.site.register(EmbeddingRequest)
admin.site.register(SectioningRequest)
admin.site.register(StainingRequestChangeLog)
admin.site.register(EmbeddingRequestChangeLog)
admin.site.register(SectioningRequestChangeLog)
