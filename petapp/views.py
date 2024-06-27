from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
import string
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated 
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pet


from .models import CustomUser,Donor,Buyer,Category,Pet
from .serializers import DonorRegistrationSerializer,BuyerRegistrationSerializer,LoginSerializer,CategorySerializer,DonorSerializer,BuyerSerializer,PetDonationSerializer,PetSerializer

@api_view(['POST'])
def register_donor(request):
    if request.method == 'POST':
        # Extract data from the request
        username = request.data.get('name')
        email = request.data.get('email')
        user_type = request.data.get('user_type')
        phone_number = request.data.get('mobile_number')
        donoraddress = request.data.get('address')
        
        # Generate a random password
        password = ''.join(random.choices(string.digits, k=6))
        
        # Create and save the User object
        user = CustomUser.objects.create(username=username, email=email, user_type=user_type)
        user.set_password(password)
        user.save()
        
        # Create and save the UserProfile object
        profile = Donor.objects.create(user=user, name=username,mobile_number=phone_number ,address=donoraddress)
        profile.save()
        
        # Send registration email
        subject = f'Registration Success'
        message = f'Username: {username}\nPassword: {password}\nEmail: {email}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        
        # Add success message
        messages.info(request, 'Registration success, please check your email for username and password..')
        
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    










@api_view(['POST'])
def register_buyer(request):
    if request.method == 'POST':
        # Extract data from the request
        username = request.data.get('name')
        email = request.data.get('email')
        user_type = request.data.get('user_type')
        phone_number = request.data.get('mobile_number')
        donoraddress = request.data.get('address')
        
        # Generate a random password
        password = ''.join(random.choices(string.digits, k=6))
        
        # Create and save the User object
        user = CustomUser.objects.create(username=username, email=email, user_type=user_type)
        user.set_password(password)
        user.save()
        
        # Create and save the UserProfile object
        profile = Buyer.objects.create(user=user, name=username,mobile_number=phone_number ,address=donoraddress)
        profile.save()
        
        # Send registration email
        subject = f'Registration Success'
        message = f'Username: {username}\nPassword: {password}\nEmail: {email}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        
        # Add success message
        messages.info(request, 'Registration success, please check your email for username and password..')
        
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    













    



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                user_type = user.user_type
                if user_type == 1:
                    role = 'Admin'
                elif user_type == 2:
                    role = 'Donor'
                else:
                    role = 'Buyer'
                # Assign a default value for unexpected user types
                refresh = RefreshToken.for_user(user)
                return JsonResponse({'access': str(refresh.access_token), 'role': role})
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









class AddCategoryAPIView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DonorListAPIView(generics.ListAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer







class DonorDeleteAPIView(generics.DestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)







class BuyerListAPIView(generics.ListAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer







class BuyerDeleteAPIView(generics.DestroyAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    




class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer  




class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer




@api_view(['POST'])
def pet_donation_create(request):
    serializer = PetDonationSerializer(data=request.data)
    if serializer.is_valid():
        # Extract category_id from request data
        category_id = request.data.get('category')
        category = get_object_or_404(Category, id=category_id)
        
        # Save pet object with category
        serializer.save(category=category)
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PetListAPIView(generics.ListAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer



class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]  # Example: Use appropriate permissions

    @action(detail=True, methods=['post'])
    def approve_pet(self, request, pk=None):
        pet = self.get_object()
        if pet.status == 'one':
            pet.status = 'two'  # Approved status
            pet.save()
            return Response({'message': 'Pet donation approved.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Pet donation cannot be approved.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def disapprove_pet(self, request, pk=None):
        pet = self.get_object()
        if pet.status == 'one':
            pet.status = 'three'  # Disapproved status
            pet.save()
            return Response({'message': 'Pet donation disapproved.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Pet donation cannot be disapproved.'}, status=status.HTTP_400_BAD_REQUEST)