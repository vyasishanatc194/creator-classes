import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking
from django.shortcuts import reverse
# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have a valid email address.")

        if not kwargs.get("username"):
            raise ValueError("Users must have a valid username.")

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get("username")
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account


class User(AbstractBaseUser, PermissionsMixin):
    flag_login = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True, unique=True)
    username = models.CharField(max_length=40, blank=True, null=True,default='')
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    profile_image = models.ImageField(upload_to="profile_image", default="sample.jpg", null=True,  blank=True, verbose_name=_("Profile Image"))
    description = models.CharField(max_length=255, blank=True)
    customer_id = models.CharField(_("Customer Id"), blank=True, max_length=255)
    plan_id = models.ForeignKey("customadmin.Plan", on_delete=models.CASCADE, related_name="selected_plan", null=True, blank=True)
    plan_purchased_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    plan_purchase_detail = models.ForeignKey("user.TransactionDetail", on_delete=models.CASCADE, related_name="plan_payment_detail", null=True, blank=True)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True, default='')
    stripe_subscription_id = models.CharField(_("Stripe subscription id"), max_length=255, blank=True, null=True)
    paypal_subscription_id = models.CharField(_("Paypal subscription id"), max_length=255, blank=True, null=True)

    country_details = models.ForeignKey('CountryField',on_delete=models.CASCADE,null=True,blank=True)

    card_id = models.CharField(_("Card Id"), max_length=255, blank=True)
    last4 = models.CharField(_("Last 4 digits"), max_length=255, blank=True)
    brand = models.CharField(_("Brand of card"), max_length=255, blank=True)
    exp_month = models.CharField(_("Exp. month"), max_length=255, blank=True)
    exp_year = models.CharField(_("Exp. year"), max_length=255, blank=True)
    card_name = models.CharField(_("Card holder name"), max_length=255, blank=True, null=True)
    affiliated_with = models.ForeignKey("creator.Creator", on_delete=models.CASCADE, null=True, blank=True)
    link_expired_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    password_reset_link = models.UUIDField(unique=True, null=True, blank=True)

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_("Unique Id"),)

    is_creator = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.email)

    def __unicode__(self):
        return self.pk

    def get_full_name(self):
        return " ".join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("customadmin:user-list")

class UserCard(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="user_credit_card_detail")
    card_number = models.CharField(max_length=19, blank=True, null=True)
    expiry_month_year = models.CharField(max_length=7, blank=True, null=True)
    stripe_token = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.card_number

    class Meta:
        verbose_name = "User Card Detail"
        verbose_name_plural = "User Card Details"
        ordering = ["-created_at"]


class UserSelectedKeyword(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="users")
    keyword = models.ForeignKey("customadmin.AdminKeyword", on_delete=models.CASCADE, related_name="user_selected_keyword")
    def __str__(self):
        return str(self.user.pk)

    class Meta:
        verbose_name = "User Selected Keyword"
        verbose_name_plural = "User Selected Keywords"
        ordering = ["-created_at"]


class UserPlanPurchaseHistory(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="plan_user")
    plan = models.ForeignKey("customadmin.Plan", on_delete=models.CASCADE, related_name="user_plan", null=True, blank=True)
    plan_purchase_detail = models.ForeignKey("user.TransactionDetail", on_delete=models.CASCADE, related_name="transaction_detail", null=True, blank=True)
    def __str__(self):
        return str(self.user.pk)

    class Meta:
        verbose_name = "Plan Purchase History"
        verbose_name_plural = "Plan Purchase History"
        ordering = ["-created_at"]


class UserKeyword(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="user_keyword")
    keyword = models.ForeignKey("customadmin.AdminKeyword", on_delete=models.CASCADE, related_name="user_selected_keywords")
    def __str__(self):
        return str(self.keyword.pk)

    class Meta:
        verbose_name = "User Keyword"
        verbose_name_plural = "User Keywords"
        ordering = ["-created_at"]