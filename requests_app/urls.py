from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Request URLs
    path('requests/', views.RequestListView.as_view(), name='request_list'),
    path('requests/create/', views.RequestCreateView.as_view(), name='request_create'),
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
    
    # Import URLs
    path('data/studies/import/', views.import_studies_from_file, name='import_studies'),
    path('data/antibodies/import/', views.import_antibodies_from_file, name='import_antibodies'),
] 