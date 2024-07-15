# Import necessary modules and models for the admin interface
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Subclass the UserAdmin class to customize the admin interface for the User model
class UserModelAdmin(BaseUserAdmin):
    
    # Override the default behavior to prevent users from creating new users
    # through the admin interface.
    def has_add_permission(self, request):
        return False

    # Override the default behavior to prevent users from deleting users
    # through the admin interface.
    def has_delete_permission(self, request, obj=None):
        return False

    # Make all fields read-only in the admin interface.
    def get_readonly_fields(self, request, obj=None):
        return self.get_fields(request, obj)

    # Define which fields to display in the admin interface
    list_display = ('id', 'username', 'is_admin', 'is_active', 'first_name', 'last_name', 'email', 'user_created')

    # Define which fields to filter by in the admin interface
    list_filter = ('is_admin',)

    # Define the fieldsets for the admin interface
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Important Dates', {'fields': ('user_created', 'last_login')}),
    )

    # Define the fields to display when adding a new user in the admin interface
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    # Define which fields to search by in the admin interface
    search_fields = ('email', 'username', 'first_name', 'last_name')

    # Define the ordering of the admin interface
    ordering = ('id',)

    # Define which fields to display horizontally in the admin interface
    filter_horizontal = ()

# Register the UserModelAdmin class with the User model for the admin interface
admin.site.register(User, UserModelAdmin)

# Register other models with default admin interfaces
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'created_at', 'updated_at')
    search_fields = ('name', 'category', 'brand')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url', 'alt_text', 'created_at', 'updated_at')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_amount', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'created_at', 'updated_at')
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at', 'updated_at')
    search_fields = ('product__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at', 'updated_at')
    search_fields = ('cart__user__username', 'product__name')
    readonly_fields = ('created_at', 'updated_at')