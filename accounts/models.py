from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models

class SiteUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ("USER","USER"),
        ("JOB_SEEKER","JOB_SEEKER"),
        ("COMPANY","COMPANY"),
    )
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        blank=False,
        null=False,
        default="USER"
        )

class JobSeekerProfile(models.Model):
    JOB_PREFERENCE_CHOICES = (
        ("PART_TIME","PART_TIME"),
        ("FULL_TIME","FULL_TIME"),
        ("ANY","ANY"),
    )
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE, related_name='job_seeker_profile')
    job_preference = models.CharField(
        max_length=20,
        choices=JOB_PREFERENCE_CHOICES,
        blank=False,
        null=False,
        default="ANY"
    )


class CompanyProfile(models.Model):
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )
    

