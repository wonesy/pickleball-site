# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from matches.models import Match


class MatchPlayerInline(admin.TabularInline):
    model = Match
    fk_name = "player"  # Specify the ForeignKey attribute to use for the inline
    extra = 0  # Set to 0 to display existing matches, set to a positive number to add empty forms for new matches.


class MatchOpponentInline(admin.TabularInline):
    model = Match
    fk_name = "opponent"  # Specify the ForeignKey attribute to use for the inline
    extra = 0  # Set to 0 to display existing matches, set to a positive number to add empty forms for new matches.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "phone",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("phone",)}),)
    inlines = [MatchPlayerInline, MatchOpponentInline]  # Combine the two inlines


# Register the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
