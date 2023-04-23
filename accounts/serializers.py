from django.forms import ValidationError
from rest_framework import serializers

from accounts.models import CompanyProfile, JobSeekerProfile, SiteUser

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self,instance):
        serializer = None
        if instance:
            if instance.account_type == dict(SiteUser.ACCOUNT_TYPE_CHOICES)["JOB_SEEKER"]:
                serializer = JobSeekerProfileValidationSerializer(instance=instance.job_seeker_profile)
            if instance.account_type == dict(SiteUser.ACCOUNT_TYPE_CHOICES)["COMPANY"]:
                serializer = CompanyProfileValidationSerializer(instance=instance.company_profile)
        data = {}
        if serializer:
            data = serializer.data
        return data
    
    def validate(self, attrs):
        serializer_class = None
        extra_data = {key: value for key,value in self.initial_data.items() if key not in self.Meta.fields}
        if attrs["account_type"] == dict(SiteUser.ACCOUNT_TYPE_CHOICES)["JOB_SEEKER"]:
            serializer_class = JobSeekerProfileValidationSerializer
        if attrs["account_type"] == dict(SiteUser.ACCOUNT_TYPE_CHOICES)["COMPANY"]:
            serializer_class = CompanyProfileValidationSerializer

        serializer = serializer_class(data=extra_data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        self.profile_validated_data = serializer.data
        
        return super().validate(attrs)
        
    def create(self, validated_data):
        user = SiteUser.objects.create_user(**validated_data)
        user.save()

        if validated_data["account_type"] == dict(SiteUser.ACCOUNT_TYPE_CHOICES)["JOB_SEEKER"]:
            JobSeekerProfile.objects.create(user=user,**self.profile_validated_data)

        if validated_data["account_type"] == dict(SiteUser.ACCOUNT_TYPE_CHOICES)["COMPANY"]:
            CompanyProfile.objects.create(user=user,**self.profile_validated_data)
        return user
    
    class Meta:
        model = SiteUser
        fields = ['id', 'username', 'email', 'password', 'account_type', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class JobSeekerProfileValidationSerializer(serializers.Serializer):
    job_preference = serializers.ChoiceField(
        choices=JobSeekerProfile.JOB_PREFERENCE_CHOICES,
        required=True
    )
    

class CompanyProfileValidationSerializer(serializers.Serializer):
    company_name = serializers.CharField(
        required=True
    )
