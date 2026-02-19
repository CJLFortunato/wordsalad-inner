from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput,min_length=8, max_length=20)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput,min_length=8, max_length=20
    )

    class Meta:
        model = User
        fields = ["email", "timezone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        if len(password1) < 8 or len(password2) < 8:
            raise ValidationError("Password must be at least 8 characters")
        if len(password1) > 20 or len(password2) > 20:
            raise ValidationError("Password must be less than 20 characters")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "is_active", "is_admin", "timezone"]


class UserManageForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    email = forms.EmailField(max_length=150, label="Email address")

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput,min_length=8, max_length=20, required=False)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput,min_length=8, max_length=20, required=False
    )

    class Meta:
        model = User
        fields = ["email", "timezone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 and not password2:
            return
        if password1 and not password2:
            raise ValidationError("Please enter the same password twice")
        if password2 and not password1:
            raise ValidationError("Please enter the same password twice")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        if len(password1) < 8 or len(password2) < 8:
            raise ValidationError("Password must be at least 8 characters")
        if len(password1) > 20 or len(password2) > 20:
            raise ValidationError("Password must be less than 20 characters")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if self.cleaned_data["password1"] is not None:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "is_admin", "timezone"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "timezone"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2", "timezone"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
