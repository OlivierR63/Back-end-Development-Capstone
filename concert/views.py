from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending


# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username=username).first()
        if user:
            return render(request,
                          'signup.html',
                          {
                              "form": SignUpForm,
                              "message": "User already exists"
                          })
        else:
            user = User.objects.create(username=username,
                                       password=make_password(password))
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "signup.html", {"form": SignUpForm})


def index(request):
    return render(request, "index.html")


def songs(request):
    songs = {"songs": [{"id": 1,
                        "title": ("duis faucibus accumsan odio "
                                  "curabitur convallis"),
                        "lyrics": ('Morbi non lectus.'
                                   ' Aliquam sit amet diam in magna bibendum'
                                   ' imperdiet. Nullam orci pede, venenatis '
                                   'non, sodales sed, tincidunt eu, felis.')
                       }]
            }
    return render(request, "songs.html", {"songs": songs["songs"]})


def photos(request):
    photos = [{
                "id": 1,
                "pic_url": "http://dummyimage.com/136x100.png/5fa2dd/ffffff",
                "event_country": "United States",
                "event_state": "District of Columbia",
                "event_city": "Washington",
                "event_date": "11/16/2022"
            }]
    return render(request, "photos.html", {"photos": photos})


def login_view(request):
    # Initializes the form. If it's a POST request, it's pre-filled with data.
    # For a GET request, it's empty.
    # The 'request' argument is necessary for AuthenticationForm.
    form = LoginForm(request,
                     data=request.POST if request.method == "POST" else None)

    if request.method == "POST":
        if form.is_valid():
            # If the form is valid, it means the user
            # has been successfully authenticated
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # If the form is not valid, it already contains errors,
        # and the code outside the 'if request.method == "POST"'
        # will handle the rendering.

    # For GET requests, or if the POST was not valid, we display
    # the login page with the form (which contains errors if the POST failed).
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def concerts(request):
    if request.user.is_authenticated:
        lst_of_concert = []
        concert_objects = Concert.objects.all()
        for item in concert_objects:
            try:
                status = item.attendee.filter(
                    user=request.user).first().attending
            except AttributeError:
                status = "-"
            lst_of_concert.append({
                "concert": item,
                "status": status
            })
        return render(request, "concerts.html", {"concerts": lst_of_concert})
    else:
        return HttpResponseRedirect(reverse("login"))


def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = Concert.objects.get(pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except AttributeError:
            status = "-"
        return render(
                        request,
                        "concert_detail.html",
                        {
                            "concert_details": obj,
                            "status": status,
                            "attending_choices":
                            ConcertAttending.AttendingChoices.choices
                        }
                    )
    else:
        return HttpResponseRedirect(reverse("login"))


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
