from rest_framework import serializers
from .models import Donor, Buyer, CustomUser,Category,Pet,Purchase


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
    email = serializers.SerializerMethodField()
    class Meta:
        model = Donor

        fields = ['id', 'user', 'name', 'email', 'mobile_number', 'address']
    def get_email(self, obj):
        return obj.user.email



class BuyerSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    class Meta:
        model = Buyer
        fields = ['id', 'user', 'name', 'email', 'mobile_number', 'address']
    def get_email(self, obj):
        return obj.user.email








class PetDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['image', 'description', 'breed', 'category', 'age', 'sex', 'weight', 'medical_conditions', 'status', 'price']




class PetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')  # Include category name

    class Meta:
        model = Pet
        fields = ['id', 'image', 'description', 'breed', 'category_name', 'age', 'sex', 'weight', 'medical_conditions', 'status', 'price','donor']










class PetCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']  




class PetdonorSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')  # Include category name
    donor_name = serializers.CharField(source='donor.username', read_only=True)  # Add donor name
    
    class Meta:
        model = Pet
        fields = ['id', 'image', 'description', 'breed', 'category_name', 'age', 'sex', 'weight', 'medical_conditions', 'status', 'price', 'donor_name']

class PurchaseSerializer(serializers.ModelSerializer):
    pet = PetdonorSerializer()  # Use PetdonorSerializer to include donor name
    buyer = BuyerSerializer()  # Use BuyerSerializer to serialize the buyer field

    class Meta:
        model = Purchase
        fields = ('id', 'pet', 'buyer', 'purchase_date', 'total_price')
    
    def create(self, validated_data):
        return Purchase.objects.create(**validated_data)
 





class DonorprofileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = Donor
        fields = ['id', 'user', 'name', 'email', 'mobile_number', 'address']

    def get_email(self, obj):
        return obj.user.email     




class BuyerprofileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = Buyer
        fields = ['id', 'user', 'name', 'email', 'mobile_number', 'address']

    def get_email(self, obj):
        return obj.user.email          