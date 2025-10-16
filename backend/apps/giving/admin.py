from django.contrib import admin
from django.utils.html import format_html
from .models import Partnership, Donation


@admin.register(Partnership)
class PartnershipAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'email', 
        'partnership_type', 
        'amount_display',
        'status',
        'is_recurring',
        'created_at'
    )
    list_filter = ('status', 'partnership_type', 'is_recurring', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'payment_reference')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Partnership Details', {
            'fields': ('partnership_type', 'amount', 'message')
        }),
        ('Payment Information', {
            'fields': (
                'status', 
                'is_recurring', 
                'next_payment_date', 
                'last_payment_date', 
                'payment_reference'
            )
        }),
    )
    
    def amount_display(self, obj):
        return f"KES {obj.amount:,.2f}" if obj.amount else "-"
    amount_display.short_description = 'Amount'
    amount_display.admin_order_field = 'amount'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email_display',
        'amount_display',
        'payment_status',
        'is_anonymous',
        'created_at'
    )
    list_filter = ('payment_status', 'is_anonymous', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'payment_reference')
    list_editable = ('payment_status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'message')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_reference')
        }),
    )
    
    def email_display(self, obj):
        return obj.email if not obj.is_anonymous else "Anonymous"
    email_display.short_description = 'Email'
    
    def amount_display(self, obj):
        return f"KES {obj.amount:,.2f}"
    amount_display.short_description = 'Amount'
    amount_display.admin_order_field = 'amount'
