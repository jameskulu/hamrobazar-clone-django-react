from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = Account
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name',
                   'last_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    readonly_field = ('date_joined', 'last_login')
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        Account.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(Account, UserAdminConfig)
