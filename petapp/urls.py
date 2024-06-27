from django.urls import path
from . import views 
from .views import LoginView
from .views import AddCategoryAPIView,DonorListAPIView,DonorDeleteAPIView,BuyerListAPIView,BuyerDeleteAPIView,CategoryListCreateView, CategoryDetailView



urlpatterns = [
    path('api/donor/register/', views.register_donor, name='register_donor'),
    path('api/buyer/register/', views.register_buyer, name='register_donor'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/categories/add/', AddCategoryAPIView.as_view(), name='add_category'),
    path('api/donors/', DonorListAPIView.as_view(), name='donor-list'),
    path('api/donors/<int:pk>/', DonorDeleteAPIView.as_view(), name='donor-delete'),
    path('api/buyers/', BuyerListAPIView.as_view(), name='buyer-list'),
    path('api/buyers/<int:pk>/', BuyerDeleteAPIView.as_view(), name='buyer-delete'),
    
    path('api/categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/pets/donate/', views.pet_donation_create, name='pet-donation-create'),
    path('api/pets/', views.PetListAPIView.as_view(), name='pet-list'),
    path('api/pets/<int:pk>/approve/', views.PetViewSet.as_view({'post': 'approve_pet'}), name='approve-pet'),
    path('api/pets/<int:pk>/disapprove/', views.PetViewSet.as_view({'post': 'disapprove_pet'}), name='disapprove-pet'),

    
    ]