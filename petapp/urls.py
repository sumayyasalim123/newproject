from django.urls import path
from . import views 
from .views import LoginView
from .views import AddCategoryAPIView,DonorListAPIView,DonorDeleteAPIView,BuyerListAPIView,BuyerDeleteAPIView,CategoryListCreateView, CategoryDetailView,ApprovedPetsListView



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
    # path('api/pets/approve/<int:pk>/', views.PetViewSet.as_view({'post': 'approve_pet'}), name='approve-pet'),
    path('api/pets/approve/<int:id>/',views.approve, name='approve'),
    # path('api/pets/disapprove/<int:pk>/', views.PetViewSet.as_view({'post': 'disapprove_pet'}), name='disapprove-pet'),
    path('api/pets/disapprove/<int:id>/',views.disapprove, name='disapprove'),
    path('api/pets/approved/', ApprovedPetsListView.as_view(), name='approved-pets-list'),
    path('api/pets/count/', views.count_status_one_pets, name='count_status_one_pets'),
    path('api/purchases/', views.create_purchase, name='create_purchase'),
    path('api/donor/purchaselist/', views.DonorPurchaseListView.as_view(), name='donor-purchase-list'),
    path('api/admin/purchases/', views.AdminPurchaseListView.as_view(), name='admin-purchases-list'),
  
     
    
    path('api/donor/profile/', views.DonorProfileView.as_view(), name='donor_profile'),
     path('api/donor/profile/edit/', views.DonorProfileEditView.as_view(), name='donor-profile-edit'),
      path('api/buyer/profile/', views.BuyerProfileView.as_view(), name='buyer_profile'),
     path('api/buyer/profile/edit/', views.BuyerProfileEditView.as_view(), name='buyer-profile-edit'),
 




    path('api/admin-profile/<int:id>/<str:username>/<int:userType>/', views.AdminProfileView.as_view(), name='admin-profile'),
    
    ]