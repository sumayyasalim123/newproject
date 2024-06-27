from rest_framework import serializers
from .models import Donor, Buyer, CustomUser,Category,Pet


class DonorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ('name', 'email', 'mobile_number', 'address')

    def create(self, validated_data):
        user_data = {
            'username': validated_data['email'],  # You can set username to email
            'email': validated_data['email'],
            'user_type': 2  # Set user_type to 2 for donor
        }
        
       
        user = CustomUser.objects.create(**user_data)
       
        user.save()
        donor = Donor.objects.create(user=user, **validated_data)
        return donor

class BuyerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ('name', 'email', 'mobile_number', 'address')

    def create(self, validated_data):
        user_data = {
            'username': validated_data['email'],  # You can set username to email
            'email': validated_data['email'],
            'user_type': 3  # Set user_type to 3 for buyer
        }
        
       
        user = CustomUser.objects.create(**user_data)
       
        user.save()
        buyer = Buyer.objects.create(user=user, **validated_data)
        return buyer
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    def validate(self, data):
        # Perform additional validation if needed
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ['id', 'user', 'name', 'email', 'mobile_number', 'address']




class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['id', 'user', 'name', 'email', 'mobile_number', 'address']







class PetDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['image', 'description', 'breed', 'category', 'age', 'sex', 'weight', 'medical_conditions', 'status']




class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'image', 'description', 'breed', 'category', 'age', 'sex', 'weight', 'medical_conditions', 'status']        