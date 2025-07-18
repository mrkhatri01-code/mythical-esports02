from django.db import models
from django.utils.safestring import mark_safe

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    game = models.CharField(max_length=100)
    prize_pool = models.CharField(max_length=100)
    date = models.DateTimeField()
    banner = models.ImageField(upload_to='tournament_banners/', help_text='Recommended size: 1200x400px')
    description = models.TextField(blank=True)
    registration_link = models.URLField(blank=True, help_text='Google Form or registration link')

    def __str__(self):
        return self.name

class TeamTournamentResult(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('INR', 'Indian Rupee'),
        ('NPR', 'Nepalese Rupee'),
    ]
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    prize_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text='Prize amount won by the team in this tournament')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    class Meta:
        unique_together = ('team', 'tournament')

    def __str__(self):
        return f"{self.team.name} - {self.tournament.name}: {self.currency} {self.prize_amount}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/', help_text='Recommended size: 300x300px')
    description = models.TextField(blank=True)
    tournaments_played = models.ManyToManyField('Tournament', blank=True, related_name='teams_played', through='TeamTournamentResult')

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    photo = models.ImageField(upload_to='player_photos/', blank=True, help_text='Recommended size: 800x800px')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def player_card(self):
        team_logo_html = ''
        if self.team and self.team.logo:
            team_logo_html = (
                '<span style="display:inline-flex;align-items:center;justify-content:center;'
                'background:#fff;border-radius:50%;width:40px;height:40px;vertical-align:middle;'
                'margin-right:8px;box-shadow:0 2px 8px rgba(0,0,0,0.07);">'
                f'<img src="{self.team.logo.url}" style="object-fit:contain;width:32px;height:32px;max-width:90%;max-height:90%;" />'
                '</span>'
            )
        html = f'''
        <div style="display:flex;align-items:center;gap:32px;">
            <div style="background:linear-gradient(135deg,#ffb86c 0%,#ff512f 100%);border-radius:50%;padding:6px;">
                <img src="{self.photo.url if self.photo else ''}" style="height:120px;width:120px;object-fit:contain;border-radius:50%;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.10);">
            </div>
            <div>
                <strong style="font-size:1.2em;">Player Information</strong><br>
                <span style="font-size:1.1em;">Name: {self.name}</span><br>
                <span style="font-size:1em;">Team: {team_logo_html}{self.team.name if self.team else ''}</span>
            </div>
        </div>
        '''
        return mark_safe(html)
    player_card.short_description = 'Player Card'

class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='sponsor_logos/', help_text='Recommended size: 200x100px')
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    banner = models.ImageField(upload_to='blog_banners/', blank=True, help_text='Recommended size: 800x400px')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ImageField(upload_to='testimonial_photos/', blank=True, help_text='Recommended size: 100x100px')

    def __str__(self):
        return self.name

class Stream(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    platform = models.CharField(choices=[('twitch', 'Twitch'), ('youtube', 'YouTube')], max_length=20)
    featured = models.BooleanField(default=False, help_text='Show this stream/video on the Streams & Videos page')

    def __str__(self):
        return self.name

class SocialLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.CharField(max_length=50, help_text='FontAwesome icon class, e.g., fab fa-twitter')

    def __str__(self):
        return self.name
