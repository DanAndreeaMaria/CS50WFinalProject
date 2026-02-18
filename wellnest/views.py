from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import date, timedelta
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
import random
import json

from .models import User, Entry, DailyCheckIn

# Create your views here.

@login_required
def index(request):
    entries = Entry.objects.filter(user=request.user).order_by("-created_at")
    today = timezone.now().date()
    entry_saved = request.GET.get("entry_saved") == "1"

    # Check if the user completed check-in today
    has_checked_in_today = DailyCheckIn.objects.filter(
        user=request.user,
        date=today
    ).exists()

    # Pagination: 5 entries per page
    paginator = Paginator(entries, 5)   # 5 per page
    page_number = request.GET.get("page")   # Get ?page=X from URL
    page_entries = paginator.get_page(page_number)

    # Today's check-in
    checkin_done = DailyCheckIn.objects.filter(
        user=request.user,
        date=date.today()
    ).first()

    return render(request, "wellnest/index.html", {
        "entry_saved": entry_saved,
        "entries": page_entries,
        "checkin_done": checkin_done,
        "show_notification": not has_checked_in_today,
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign in the user
        username = request.POST["username"]
        password = request.POST["password"]

        # Check for empty fields
        if not username:
            return render(request, "wellnest/login.html", {
                "message": "Please enter a username."
            })
        
        if not password:
            return render(request, "wellnest/login.html", {
                "message": "Please enter a password."
            })
        
        # Attempt to sign in the user
        user = authenticate(request, username=username, password=password)

        #Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "wellnest/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "wellnest/login.html")
    

def logout_view(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        # Ensure password matches confirmation
        password = request.POST.get("password", "").strip()
        confirmation = request.POST.get("confirmation", "").strip()

        # Check that all fields are filled        
        if not username:
            return render(request, "wellnest/register.html", {
                "message": "Please enter a username."
            })
        
        if not password:
            return render(request, "wellnest/register.html", {
                "message": "Password cannot be empty."
            })
        
        if not confirmation:
            return render(request, "wellnest/register.html", {
                "message": "Please enter the confirmation."
            })

        if password != confirmation:
            return render(request, "wellnest/register.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create a new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "wellnest/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "wellnest/register.html")
    

@login_required
def new_entry(request):
    # Get today's date
    today = timezone.now().date()

    # Check if the user already completed the daily check-in
    has_checked_in_today = DailyCheckIn.objects.filter(
        user=request.user,
        date=today
    ).exists()

    # Creates the new entry
    if request.method == "POST":
        mood = request.POST["mood"]
        quality = request.POST["quality"]
        text = request.POST["text"]

        Entry.objects.create(
            user=request.user,
            mood=mood,
            quality=quality,
            text=text
        )

        return redirect("index")
    
    return render(request, "wellnest/new_entry.html", {
        "show_notification": not has_checked_in_today
    })


@login_required
def daily_checkin(request):
    # Get today's date 
    today = timezone.now().date()

    # Check if the user already completed today's check-in
    existing_checkin = DailyCheckIn.objects.filter(
        user=request.user,
        date=today
    ).first()

    # True or false
    has_checked_in_today = existing_checkin is not None

    # Handle form submission
    if request.method == "POST":
        # Prevent duplicate check-ins
        if existing_checkin:
            return redirect("index") 

        # Create new check-in
        DailyCheckIn.objects.create(
            user=request.user,
            date=today,
            mood=request.POST["mood"],
            energy=request.POST["energy"],
            stress=request.POST["stress"],
            sleep=request.POST["sleep"],
            social=request.POST["social"],
            activity=request.POST['activity'],
        )
        return redirect("index")
    
    # Render page
    return render(request, "wellnest/daily_checkin.html", {
        # Used to show "already completed" message
        "checkin_done": has_checked_in_today,
        # Used for notification bell
        "show_notification": not has_checked_in_today
    })


@login_required
def analysis(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # Check if the user already completed daily check-in
    has_checked_in_today = DailyCheckIn.objects.filter(
        user=request.user,
        date=today
    ).exists()

    # Helper function for naming the values
    def scale_label(value):
        if value is None:
            return None
        if value < 2:
            return "very low"
        elif value < 3:
            return "low"
        elif value < 4:
            return "okay"
        elif value < 4.5:
            return "good"
        else:
            return "very good"
        
    # Trend detection
    def trend(values):
        # If there's only 1 value
        if len(values) < 2:
            return "stable"
        if values[-1] > values[0]:
            return "improving"
        elif values [-1] < values[0]:
            return "declining"
        return "stable"
    
    # Get last 7 days of check-ins
    checkins = DailyCheckIn.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).order_by("date")
    # Get check-ins whose date is greater than or equal to 7 days ago

    # If there's not enough data, it will be handled
    if checkins.count() < 3:
        return render(request, "wellnest/analysis.html", {
            "not_enough_data": True
        })
    
    # Prepare data for charts
    dates = []
    mood_values = []
    energy_values = []
    stress_values = []
    sleep_values = []
    suggestions = []
    social_values = []
    activity_values = []

    for checkin in checkins:
        dates.append(checkin.date.strftime("%Y-%m-%d"))
        mood_values.append(checkin.mood)
        energy_values.append(checkin.energy)
        stress_values.append(checkin.stress)
        sleep_values.append(checkin.sleep)
        social_values.append(checkin.social)
        activity_values.append(checkin.activity)
    
    # Calculate averages
    total_mood = 0
    total_energy = 0
    total_stress = 0
    total_sleep = 0
    total_social = 0
    total_activity = 0

    for checkin in checkins:
        total_mood += checkin.mood
        total_energy += checkin.energy
        total_stress += checkin.stress
        total_sleep += checkin.sleep
        total_social += checkin.social
        total_activity += checkin.activity

    count = checkins.count()

    # Weekly averages for suggestions
    averages = {
        "mood": round(total_mood / count, 2),
        "energy": round(total_energy / count, 2),
        "stress": round(total_stress / count, 2),
        "sleep": round(total_sleep / count, 2),
        "social": round(total_social / count, 2),
        "activity": round(total_activity / count, 2),
    }

    # Daily encouragements (for today's values)
    today_sleep = sleep_values[-1]
    today_mood = mood_values[-1]
    today_energy = energy_values[-1]
    today_stress = stress_values[-1]

    labels = {
        "mood": scale_label(averages["mood"]),
        "energy": scale_label(averages["energy"]),
        "stress": scale_label(averages["stress"]),
        "sleep": scale_label(averages["sleep"]),
        "social": scale_label(averages["social"]),
        "activity": scale_label(averages["activity"]),
    }
    
    trends = {
        "mood": trend(mood_values),
        "energy": trend(energy_values),
        "stress": trend(stress_values),
        "sleep": trend(sleep_values),
        "social": trend(social_values),
        "activity": trend(activity_values),
    }

    # Soft suggestions for weekly averages
    if averages["sleep"] and averages["sleep"] < 3:
        suggestions.append(
            "Your sleep has been on the lower side. Rest might help support your energy and mood 🌱"
        )
    elif averages["sleep"] >= 4:
        suggestions.append(
            "Your sleep has been fairly consistent and supportive lately. That's a solid foundation for your wellbeing 💤"
        )

    if averages["stress"] and averages["stress"] > 4:
        suggestions.append(
            "Stress levels have been high lately. Gentle breaks or breathing exercises could help."
        )

    # Daily random generated encouragement messages, single and combined
    sleep_messages = [
        "You slept well last night - that's a meaningful step for your daily wellbeing! 💤",
        "Rest looks supportive! Your body appreciates that 🌚",
        "Good sleep creates strong foundations. Keep nurturing this rhythm 🌟"
    ]

    mood_messages = [
        "Your mood feels positive. Notice what's supporting that! 🌞",
        "You're in good spirits - maybe take a moment to celebrate the little joys of life! 🌷",
        "Happiness is present! Make sure you spread the good vibes to others! 🎈"
    ]

    energy_messages = [
        "Your energy feels strong. It might be a beautiful moment to do something that nourishes you ⚡",
        "You feel energized - a perfect opportunity to try something new! ⭐",
        "Energy levels look strong! A good moment for movement or creativity! 🌻"
    ]

    combo_messages = [
        "You're well-rested and energized on this day - that's a powerful combination! 🌱",
        "Strong sleep and strong energy - your body feels aligned today! 💜",
        "Rest and vitality are working together - truly a beautiful balance! ⚡"
    ]

    if today_mood >= 4 and today_energy >= 4:
        suggestions.append(random.choice(combo_messages))

    if today_sleep >= 4:
        suggestions.append(random.choice(sleep_messages))

    if today_mood >= 4:
        suggestions.append(random.choice(mood_messages))

    if today_energy >= 4:
        suggestions.append(random.choice(energy_messages))
    
    # Make sure we keep the app clean on suggestions
    suggestions = suggestions[:3]

    return render(request, "wellnest/analysis.html", {
        "not_enough_data": False,
        "averages": averages,
        "checkin_count": count,
        "dates": json.dumps(dates),
        "mood_values": json.dumps(mood_values),
        "energy_values": json.dumps(energy_values),
        "stress_values": json.dumps(stress_values),
        "sleep_values": json.dumps(sleep_values),
        "labels": labels,
        "trends": trends,
        "suggestions": suggestions,
        "show_notification": not has_checked_in_today
    })

def about(request):
    # Default value - no notification
    show_notification = False

    # Only check if the user is logged in
    if request.user.is_authenticated:

        today = timezone.now().date()

        has_checked_in_today = DailyCheckIn.objects.filter(
            user=request.user,
            date=today
        ).exists()

        show_notification = not has_checked_in_today

    return render(request, "wellnest/about.html", {
        "show_notification": show_notification
    })