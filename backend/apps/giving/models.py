from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class Partnership(TimeStampedModel):
    """Model for tracking ministry partnerships and giving"""
    class PartnershipType(models.TextChoices):
        MONTHLY = 'monthly', _('Monthly')
        QUARTERLY = 'quarterly', _('Quarterly')
        YEARLY = 'yearly', _('Yearly')
        ONE_TIME = 'one_time', _('One Time')
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
    
    full_name = models.CharField(_('full name'), max_length=200)
    email = models.EmailField(_('email address'))
    phone_number = models.CharField(_('phone number'), max_length=20)
    partnership_type = models.CharField(
        _('partnership type'),
        max_length=20,
        choices=PartnershipType.choices,
        default=PartnershipType.ONE_TIME
    )
    amount = models.DecimalField(
        _('amount'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Amount in KES')
    )
    message = models.TextField(_('message'), blank=True)
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    is_recurring = models.BooleanField(
        _('is recurring'),
        default=False,
        help_text=_('Whether this is a recurring payment')
    )
    next_payment_date = models.DateField(
        _('next payment date'),
        null=True,
        blank=True,
        help_text=_('Next payment date for recurring partnerships')
    )
    last_payment_date = models.DateField(
        _('last payment date'),
        null=True,
        blank=True,
        help_text=_('Date of the last successful payment')
    )
    payment_reference = models.CharField(
        _('payment reference'),
        max_length=100,
        blank=True,
        help_text=_('Reference number from payment processor')
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Partnership')
        verbose_name_plural = _('Partnerships')
    
    def __str__(self):
        return f"{self.full_name} - {self.get_partnership_type_display()}"
    
    def save(self, *args, **kwargs):
        # Set is_recurring based on partnership type
        self.is_recurring = self.partnership_type != self.PartnershipType.ONE_TIME
        super().save(*args, **kwargs)


class Donation(TimeStampedModel):
    """Model for tracking one-time donations"""
    full_name = models.CharField(_('full name'), max_length=200)
    email = models.EmailField(_('email address'))
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    amount = models.DecimalField(
        _('amount'),
        max_digits=10,
        decimal_places=2,
        help_text=_('Amount in KES')
    )
    message = models.TextField(_('message'), blank=True)
    is_anonymous = models.BooleanField(
        _('is anonymous'),
        default=False,
        help_text=_('Whether to keep the donation anonymous')
    )
    payment_reference = models.CharField(
        _('payment reference'),
        max_length=100,
        blank=True,
        help_text=_('Reference number from payment processor')
    )
    payment_status = models.CharField(
        _('payment status'),
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('completed', _('Completed')),
            ('failed', _('Failed')),
            ('refunded', _('Refunded')),
        ],
        default='pending'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Donation')
        verbose_name_plural = _('Donations')
    
    def __str__(self):
        return f"{self.full_name} - KES {self.amount}"
