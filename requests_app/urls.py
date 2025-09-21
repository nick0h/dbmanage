from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Request URLs
    path('requests/', views.RequestHomeView.as_view(), name='requests_home'),
    path('requests_home/', views.SimpleRequestHomeView.as_view(), name='simple_requests_home'),
    path('requests/list/', views.RequestListView.as_view(), name='request_list'),
    path('requests/<int:pk>/', views.RequestDetailView.as_view(), name='request_detail'),
    path('requests/<int:pk>/edit/', views.RequestUpdateView.as_view(), name='request_edit'),
    path('requests/<int:pk>/delete/', views.RequestDeleteView.as_view(), name='request_delete'),
    path('requests/search/', views.RequestSearchView.as_view(), name='request_search'),

    
    # Study URLs
    path('data/studies/<int:pk>/edit/', views.StudyUpdateView.as_view(), name='study_edit'),
    path('data/studies/<int:pk>/delete/', views.StudyDeleteView.as_view(), name='study_delete'),
    path('data/studies/', views.StudyListView.as_view(), name='study_list'),
    path('data/studies/create/', views.study_create, name='study_create'),
    
    # Data Management URLs
    path('data/', views.data_management, name='data_management'),
    
    # Requestor URLs
    path('data/requestors/', views.RequestorListView.as_view(), name='requestor_list'),
    path('data/requestors/create/', views.requestor_create, name='requestor_create'),
    path('data/requestors/<int:pk>/edit/', views.RequestorUpdateView.as_view(), name='requestor_edit'),
    path('data/requestors/<int:pk>/delete/', views.RequestorDeleteView.as_view(), name='requestor_delete'),
    
    # Antibody URLs
    path('data/antibodies/', views.AntibodyListView.as_view(), name='antibody_list'),
    path('data/antibodies/create/', views.antibody_create, name='antibody_create'),
    path('data/antibodies/<int:pk>/edit/', views.AntibodyUpdateView.as_view(), name='antibody_edit'),
    path('data/antibodies/<int:pk>/delete/', views.AntibodyDeleteView.as_view(), name='antibody_delete'),
    
    # Tissue URLs
    path('data/tissues/', views.TissueListView.as_view(), name='tissue_list'),
    path('data/tissues/create/', views.tissue_create, name='tissue_create'),
    path('data/tissues/<int:pk>/edit/', views.TissueUpdateView.as_view(), name='tissue_edit'),
    path('data/tissues/<int:pk>/delete/', views.TissueDeleteView.as_view(), name='tissue_delete'),
    
    # Status URLs
    path('data/statuses/', views.StatusListView.as_view(), name='status_list'),
    path('data/statuses/create/', views.status_create, name='status_create'),
    path('data/statuses/<int:pk>/edit/', views.StatusUpdateView.as_view(), name='status_edit'),
    path('data/statuses/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
    
    # Assignee URLs
    path('data/assignees/', views.AssigneeListView.as_view(), name='assignee_list'),
    path('data/assignees/create/', views.assignee_create, name='assignee_create'),
    path('data/assignees/<int:pk>/edit/', views.AssigneeUpdateView.as_view(), name='assignee_edit'),
    path('data/assignees/<int:pk>/delete/', views.AssigneeDeleteView.as_view(), name='assignee_delete'),
    
    # Probe URLs
    path('data/probes/', views.ProbeListView.as_view(), name='probe_list'),
    path('data/probes/create/', views.probe_create, name='probe_create'),
    path('data/probes/<int:pk>/edit/', views.ProbeUpdateView.as_view(), name='probe_edit'),
    path('data/probes/<int:pk>/delete/', views.ProbeDeleteView.as_view(), name='probe_delete'),
    
    # Priority URLs
    path('data/priorities/', views.PriorityListView.as_view(), name='priority_list'),
    path('data/priorities/create/', views.priority_create, name='priority_create'),
    path('data/priorities/<int:pk>/edit/', views.PriorityUpdateView.as_view(), name='priority_edit'),
    path('data/priorities/<int:pk>/delete/', views.PriorityDeleteView.as_view(), name='priority_delete'),
    
    # Import URLs
    path('data/studies/import/', views.import_studies_from_file, name='import_studies'),
    path('data/antibodies/import/', views.import_antibodies_from_file, name='import_antibodies'),
    
    # Request Type Specific URLs (All Requests)
    path('staining/', views.StainingRequestsView.as_view(), name='staining_requests'),
    path('embedding/', views.EmbeddingRequestsView.as_view(), name='embedding_requests'),
    path('sectioning/', views.SectioningRequestsView.as_view(), name='sectioning_requests'),
    
    # Request Type Current URLs (Filtered - Exclude Complete)
    path('staining/current/', views.StainingRequestsCurrentView.as_view(), name='staining_requests_current'),
    path('embedding/current/', views.EmbeddingRequestsCurrentView.as_view(), name='embedding_requests_current'),
    path('sectioning/current/', views.SectioningRequestsCurrentView.as_view(), name='sectioning_requests_current'),
    
    # Request Type Create URLs
    path('staining/create/', views.StainingRequestCreateView.as_view(), name='staining_request_create'),
    path('embedding/create/', views.EmbeddingRequestCreateView.as_view(), name='embedding_request_create'),
    path('sectioning/create/', views.SectioningRequestCreateView.as_view(), name='sectioning_request_create'),
    
    # Request Type Detail URLs
    path('staining/<int:pk>/', views.StainingRequestDetailView.as_view(), name='staining_request_detail'),
    path('embedding/<int:pk>/', views.EmbeddingRequestDetailView.as_view(), name='embedding_request_detail'),
    path('sectioning/<int:pk>/', views.SectioningRequestDetailView.as_view(), name='sectioning_request_detail'),
    
    # Request Type Edit URLs
    path('staining/<int:pk>/edit/', views.StainingRequestEditView.as_view(), name='staining_request_edit'),
    path('embedding/<int:pk>/edit/', views.EmbeddingRequestEditView.as_view(), name='embedding_request_edit'),
    path('sectioning/<int:pk>/edit/', views.SectioningRequestEditView.as_view(), name='sectioning_request_edit'),
    
    # Request Type Delete URLs
    path('staining/<int:pk>/delete/', views.StainingRequestDeleteView.as_view(), name='staining_request_delete'),
    path('embedding/<int:pk>/delete/', views.EmbeddingRequestDeleteView.as_view(), name='embedding_request_delete'),
    path('sectioning/<int:pk>/delete/', views.SectioningRequestDeleteView.as_view(), name='sectioning_request_delete'),
    
    # Request Type Search URLs
    path('staining/search/', views.StainingRequestSearchView.as_view(), name='staining_request_search'),
    path('embedding/search/', views.EmbeddingRequestSearchView.as_view(), name='embedding_request_search'),
    path('sectioning/search/', views.SectioningRequestSearchView.as_view(), name='sectioning_request_search'),
    
    # Request Type Delete List URLs
    path('staining/delete/', views.StainingRequestsDeleteView.as_view(), name='staining_requests_delete'),
    path('embedding/delete/', views.EmbeddingRequestsDeleteView.as_view(), name='embedding_requests_delete'),
    path('sectioning/delete/', views.SectioningRequestsDeleteView.as_view(), name='sectioning_requests_delete'),
    
    # Request Log Selection URL
    path('logs/', views.RequestLogSelectionView.as_view(), name='request_log_selection'),
    
    # Request History URLs
    path('staining/<int:pk>/history/', views.StainingRequestHistoryView.as_view(), name='staining_request_history'),
    path('embedding/<int:pk>/history/', views.EmbeddingRequestHistoryView.as_view(), name='embedding_request_history'),
    path('sectioning/<int:pk>/history/', views.SectioningRequestHistoryView.as_view(), name='sectioning_request_history'),
] 