from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
import json
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view, permission_classes
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
from rest_framework.permissions import IsAdminUser


from .models import CustomUser,Donor,Buyer,Category,Pet,Purchase
from .serializers import DonorRegistrationSerializer,BuyerRegistrationSerializer,LoginSerializer,CategorySerializer,DonorSerializer,BuyerSerializer,PetDonationSerializer,PetSerializer,PetCountSerializer,CustomUserSerializer,PurchaseSerializer,DonorprofileSerializer

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
@permission_classes([IsAuthenticated])
def pet_donation_create(request):
    serializer = PetDonationSerializer(data=request.data)
    if serializer.is_valid():
        category_id = request.data.get('category')
        category = get_object_or_404(Category, id=category_id)
        
        # Ensure the authenticated user is a donor
        if request.user.is_authenticated and request.user.user_type == 2:
            donor_user = request.user  # Retrieve the CustomUser instance
            donor_profile = donor_user.donor  # Assuming Donor model is linked via OneToOneField
            
            # Save pet object with category and donor profile (CustomUser instance)
            serializer.save(category=category, donor=donor_user)
            
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User must be authenticated as a donor'}, status=status.HTTP_403_FORBIDDEN)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PetListAPIView(generics.ListAPIView):
    serializer_class = PetSerializer

    def get_queryset(self):
        return Pet.objects.filter(status='one')


@api_view(['POST'])
def approve(request,id):
    try:
         user = Pet.objects.get(id=id)
         user.status = 'Two'
         user.save()
         return Response({'status': 'User approved'}, status=status.HTTP_200_OK)
    except Pet.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def disapprove(request,id):
    try:
         user = Pet.objects.get(id=id)
         user.status = 'Three'
         user.save()
         return Response({'status': 'User approved'}, status=status.HTTP_200_OK)
    except Pet.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    


class ApprovedPetsListView(generics.ListAPIView):
    queryset = Pet.objects.filter(status='two')
    serializer_class = PetSerializer
    



@api_view(['GET'])
def count_status_one_pets(request):
    try:
        count = Pet.objects.filter(status='one').count()
        serializer = PetCountSerializer({'count': count})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    







class AdminProfileView(APIView):
    def get(self, request, id, username, userType):
        try:
            admin = CustomUser.objects.get(id=id, username=username, user_type=userType)
            serializer = CustomUserSerializer(admin)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Admin not found."}, status=status.HTTP_404_NOT_FOUND)
        




User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_purchase(request):
    pet_id = request.data.get('pet_id')
    total_price = request.data.get('total_price')

    # Validate input
    if not pet_id or not total_price:
        return Response({'error': 'Both pet_id and total_price are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve the pet object
    pet = get_object_or_404(Pet, pk=pet_id)

    # Retrieve the buyer (assuming Buyer model is related to CustomUser)
    buyer = get_object_or_404(Buyer, user=request.user)

    # Example of creating a Purchase instance
    purchase = Purchase.objects.create(
        pet=pet,
        buyer=buyer,
        total_price=total_price,
    )

    serializer = PurchaseSerializer(purchase)

    return Response(serializer.data, status=status.HTTP_201_CREATED)





class DonorPurchaseListView(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the currently authenticated donor (CustomUser instance)
        donor = self.request.user

        # Fetch pets donated by the donor
        donated_pets = Pet.objects.filter(donor=donor)

        # Fetch purchases for those donated pets
        purchases = Purchase.objects.filter(pet__in=donated_pets)

        # Count of purchases
        purchase_count = purchases.count()

        # Add purchase count to the context
        self.request.session['purchase_count'] = purchase_count

        return purchases
    


class AdminPurchaseListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        purchases = Purchase.objects.all()
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)    
    





class DonorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        donor = request.user.donor
        serializer = DonorprofileSerializer(donor)
        return Response(serializer.data)



class DonorProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        donor = request.user  # Assuming request.user is the logged-in CustomUser object
        
        try:
            donor_profile = donor.donor  # Access the donor profile via OneToOneField
        except Donor.DoesNotExist:
            return Response({'error': 'Donor profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = json.loads(request.body)
        
        # Update fields if provided in the request data
        if 'email' in data:
            donor_profile.email = data['email']
        if 'mobile_number' in data:
            donor_profile.mobile_number = data['mobile_number']
        if 'address' in data:
            donor_profile.address = data['address']
        if 'name' in data:
            donor_profile.name = data['name']
        
        donor_profile.save()
        
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    




class BuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer = request.user.buyer
        serializer = DonorprofileSerializer(buyer)
        return Response(serializer.data)








class BuyerProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        buyer = request.user  # Assuming request.user is the logged-in CustomUser object
        
        try:
            buyer_profile = buyer.buyer  # Access the donor profile via OneToOneField
        except Buyer.DoesNotExist:
            return Response({'error': 'Buyer profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = json.loads(request.body)
        
        # Update fields if provided in the request data
        if 'email' in data:
            buyer_profile.email = data['email']
        if 'mobile_number' in data:
            buyer_profile.mobile_number = data['mobile_number']
        if 'address' in data:
            buyer_profile.address = data['address']
        if 'name' in data:
            buyer_profile.name = data['name']
        
        buyer_profile.save()
        
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    


