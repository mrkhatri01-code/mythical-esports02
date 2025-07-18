from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Tournament, Team, Player, Sponsor, Subscriber, BlogPost, Testimonial, Stream, SocialLink
from .forms import SubscriberForm, ContactForm

# Create your views here.

def home(request):
    from django.db.models import Sum
    next_tournament = Tournament.objects.filter(date__gte=timezone.now()).order_by('date').first()
    sponsors = Sponsor.objects.all()
    testimonials = Testimonial.objects.all()
    streams = Stream.objects.all()
    featured_streams = Stream.objects.filter(featured=True)
    social_links = SocialLink.objects.all()
    tournaments_count = Tournament.objects.count()
    teams_count = Team.objects.count()
    prize_pool_sum = Tournament.objects.aggregate(total=Sum('prize_pool'))['total']
    return render(request, 'core/home.html', {
        'next_tournament': next_tournament,
        'sponsors': sponsors,
        'testimonials': testimonials,
        'streams': streams,
        'featured_streams': featured_streams,
        'social_links': social_links,
        'tournaments_count': tournaments_count,
        'teams_count': teams_count,
        'prize_pool_sum': prize_pool_sum,
    })

def tournaments(request):
    tournaments = Tournament.objects.order_by('-date')
    return render(request, 'core/tournaments.html', {'tournaments': tournaments})

def teams(request):
    teams = Team.objects.all()
    return render(request, 'core/teams.html', {'teams': teams})

def players(request):
    players = Player.objects.all()
    return render(request, 'core/players.html', {'players': players})

def player_detail(request, pk):
    
    from .models import Player
    from django.shortcuts import get_object_or_404
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'core/player_detail.html', {'player': player})

def sponsors(request):
    sponsors = Sponsor.objects.all()
    return render(request, 'core/sponsors.html', {'sponsors': sponsors})

def blog_list(request):
    posts = BlogPost.objects.order_by('-created_at')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'core/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'core/blog_detail.html', {'post': post})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Send email
            send_mail(
                'New Contact Form Submission',
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                [settings.DEFAULT_FROM_EMAIL],
            )
            return render(request, 'core/contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally: sync with Mailchimp here
            return redirect('home')
    return redirect('home')

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    players = team.players.all()
    results = team.teamtournamentresult_set.select_related('tournament').all()
    return render(request, 'core/team_detail.html', {'team': team, 'players': players, 'results': results})

def streams_list(request):
    streams = Stream.objects.all()
    return render(request, 'core/streams.html', {'streams': streams})
