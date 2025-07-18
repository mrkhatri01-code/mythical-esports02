from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Tournament, Team, Player, Sponsor, Subscriber, Contact, BlogPost, Testimonial, Stream, SocialLink, TeamTournamentResult

User = get_user_model()

ALLOWED_CORE_ADMINS = [
    'admin@khatriprabhakar.com.np',
    'admin@mythical-esports.com',
]

def is_core_admin(user):
    return user.is_superuser or (hasattr(user, 'email') and user.email in ALLOWED_CORE_ADMINS)

class CustomUserAdmin(DefaultUserAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj and obj.email == 'admin@khatriprabhakar.com.np':
            return False
        return super().has_delete_permission(request, obj)

# Restrict core model admin to allowed admins only
def core_admin_permission(method):
    def wrapper(self, request, obj=None):
        return is_core_admin(request.user)
    return wrapper

class CoreAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_staff
    has_add_permission = core_admin_permission(lambda self, request: True)
    has_change_permission = core_admin_permission(lambda self, request, obj=None: True)
    has_delete_permission = core_admin_permission(lambda self, request, obj=None: True)

class PlayerAdmin(CoreAdmin):
    list_display = ('name', 'team', 'player_card')
    readonly_fields = ('player_card',)

class TeamTournamentResultInline(admin.TabularInline):
    model = TeamTournamentResult
    extra = 1

class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ()
    inlines = [TeamTournamentResultInline]

class TournamentAdmin(CoreAdmin):
    inlines = [TeamTournamentResultInline]
    class Media:
        js = ('core/admin_tournament_currency.js',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Sponsor, CoreAdmin)
admin.site.register(Subscriber, CoreAdmin)
admin.site.register(Contact, CoreAdmin)
admin.site.register(BlogPost, CoreAdmin)
admin.site.register(Testimonial, CoreAdmin)
admin.site.register(Stream, CoreAdmin)
admin.site.register(SocialLink, CoreAdmin)
admin.site.register(TeamTournamentResult, CoreAdmin)
