from rest_framework import serializers
from .models import User, Profile, Comment, Module, Session, Announcement,AnnounComment
from django.contrib.auth import authenticate
import re
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    profile='ProfileSerializer(many=False,read_only=True)'
    class Meta:
        model = User
        # fields='__all__'
        fields = ['pk','email','profile','name','user_type']
        extra_kwargs={
            "profile":{'read_only':True}
        }

class ModuleSerializer(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)
    technical_mentor_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = Module
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    modules = ModuleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)
    technical_mentor_id = serializers.IntegerField(write_only = True)
    module = ModuleSerializer(read_only=True)
    module_id = serializers.IntegerField(write_only = True)
    # session_comments = CommentSerializer(read_only = True)
    no_hours = serializers.CharField(read_only =True)

    class Meta:
        model = Session
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)
    technical_mentor_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = Announcement
        fields = "__all__"

   
class AnnouncementCommentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only = True)
    announcement=AnnouncementSerializer(read_only = True)
    announcement_id = serializers.IntegerField(write_only = True)
    likes= UserSerializer(read_only = True,many=True)
    
    class Meta:
        model=AnnounComment
        fields='__all__'
        


class CommentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only = True)
    session=SessionSerializer(read_only = True)
    session_id = serializers.IntegerField(write_only = True)
    liked_by = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all())

    class Meta:
        model=Comment
        fields='__all__'
        

    def update(self, instance, validated_data):
        liked_by = validated_data.pop('liked_by')
        for i in liked_by:
            instance.liked_by.add(i)
        instance.save()
        return instance




class UpdateProfileSerializer(serializers.ModelSerializer):
   
    user = UserSerializer(read_only=True,many=False)
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs={
            "modules":{"read_only":True}
        }


    def get_profile(self,instance,data):
        instance.bio = data.get('bio', instance.bio)
        instance = super().get_fields(instance, data)
        return instance

    def update(request, instance, validated_data):
        instance.bio = validated_data['bio']

        instance.save()
        instance=super().update(instance,validated_data)
        return instance




class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)


    
    def validate_user(self):
        email = self.validated_data["email"]
        regex = "@([a-z\S]+)"
        result = re.split(regex, email)
        # Check if the emails are from moringa
        if result[1] == "student.moringaschool.com" or result[1] == "moringaschool.com":
            new_user = authenticate(
                email=self.validated_data["email"],
                password=self.validated_data["password"],
            )
            if new_user is not None:
                return new_user
            raise serializers.ValidationError("The User does not Exist")

        raise serializers.ValidationError('Invalid Email ')


# User create serializer
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = self.validated_data["email"]
        regex = "@([a-z\S]+)"
        result = re.split(regex, email)
        # Check if the emails are from moringa
        if result[1] == "student.moringaschool.com" or result[1] == "moringaschool.com":
            user = User.objects.create_user(**validated_data)
            
            return user

        serializers.ValidationError('Invalid Email')


# Changing the password
class ChangePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

            
    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance