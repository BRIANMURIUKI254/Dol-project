from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum
from django.contrib.auth import get_user_model
from apps.events.models import Event
from apps.giving.models import Donation

User = get_user_model()

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        # Get user statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Get donation statistics
        total_donations = Donation.objects.count()
        monthly_revenue = Donation.objects.filter(
            created_at__month=timezone.now().month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get event statistics
        total_events = Event.objects.count()
        
        # Calculate conversion rate (example: percentage of users who donated)
        conversion_rate = 0
        if total_users > 0:
            donating_users = Donation.objects.values('user').distinct().count()
            conversion_rate = round((donating_users / total_users) * 100, 1)
        
        # Get recent activities (example: last 5 donations)
        recent_donations = Donation.objects.select_related('user').order_by('-created_at')[:5]
        recent_activities = [
            {
                'id': d.id,
                'user': f"{d.user.first_name} {d.user.last_name}",
                'action': f'made a donation of ${d.amount:.2f}',
                'time': self._time_ago(d.created_at)
            }
            for d in recent_donations
        ]
        
        # Get top donors
        top_donors = Donation.objects.values(
            'user__id', 'user__first_name', 'user__last_name'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')[:5]
        
        top_donors_list = [
            {
                'id': d['user__id'],
                'name': f"{d['user__first_name']} {d['user__last_name']}",
                'amount': float(d['total']),
                'avatar': ''
            }
            for d in top_donors
        ]
        
        data = {
            'totalUsers': total_users,
            'activeUsers': active_users,
            'totalDonations': total_donations,
            'totalEvents': total_events,
            'monthlyRevenue': float(monthly_revenue),
            'conversionRate': conversion_rate,
            'recentActivities': recent_activities,
            'topDonors': top_donors_list
        }
        
        return Response(data)
    
    def _time_ago(self, dt):
        now = timezone.now()
        diff = now - dt
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"
