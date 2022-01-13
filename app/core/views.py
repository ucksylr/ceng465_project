from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError


def events(request):
    events = [event.serialize() for event in Event.objects.all()]
    return JsonResponse({"events": events}, status=200)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Attempt to sign user in
        username = data.get("username", "")
        password = data.get("password", "")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({"user": user.serialize()}, status=200)
        else:
            return JsonResponse({
                "message": "Invalid username and/or password."
            }, status=200)
    else:
        return JsonResponse({"message": "Your request was invalid. POST request required."}, status=400)


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Attempt to sign user in
        username = data.get("username", "")
        email = data.get("email", "")

        # Ensure password matches confirmation
        password = data.get("password", "")
        confirmation = data.get("confirmation", "")
        if password != confirmation:
            return JsonResponse({
                "message": "Passwords must match."
            }, status=200)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return JsonResponse({
                "message": "Username already taken."
            }, status=200)
        login(request, user)
        return JsonResponse({"message": "Registered successfully."}, status=200)
    else:
        return JsonResponse({"message": "Your request was invalid. POST request required."}, status=400)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out."}, status=200)


@csrf_exempt
def add_event(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "You have to login first."}, status=200)
        if not request.user.has_perm('add_event'):
            return JsonResponse({"message": "You do not have permission to add event."}, status=200)
        data = json.loads(request.body)
        # Attempt to sign user in
        name = data.get("name", "")
        description = data.get("description", "")
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")
        event, _ = Event.objects.get_or_create(
            name=name, description=description, start_date=start_date, end_date=end_date)
        event.save()
        return JsonResponse({"message": "Event added successfully."}, status=200)
    else:
        return JsonResponse({"message": "Your request was invalid. POST request required."}, status=400)


@csrf_exempt
def delete_event(request, id):
    if request.method == "DELETE":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "You have to login first."}, status=200)
        if not request.user.has_perm('delete_event'):
            return JsonResponse({"message": "You do not have permission to delete event."}, status=200)
        event = Event.objects.get(id=id)
        event.delete()
        return JsonResponse({"message": f"Event deleted successfully. Event: {event.name}"}, status=200)
    else:
        return JsonResponse({"message": "Your request was invalid. DELETE request required."}, status=400)


@csrf_exempt
def update_event(request, id):
    if request.method == "PATCH":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "You have to login first."}, status=200)
        if not request.user.has_perm('change_event'):
            return JsonResponse({"message": "You do not have permission to update event."}, status=200)
        event = Event.objects.filter(id=id)
        if len(event) == 0:
            return JsonResponse({"message": f"Event not found. Id: {id}"}, status=200)
        data = json.loads(request.body)
        name = data.get("name", "")
        description = data.get("description", "")
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")
        print(data)
        event.update(
            name=name, description=description, start_date=start_date, end_date=end_date)
        return JsonResponse({"message": f"Event updated successfully. Event: {name}"}, status=200)
    else:
        return JsonResponse({"message": "Your request was invalid. PATCH request required."}, status=400)


def enroll(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "You have to login first."}, status=200)
    if not request.user.has_perm('can_enroll_event'):
        return JsonResponse({"message": "You do not have permission to enroll event."}, status=200)
    event = Event.objects.get(id=id)
    event.attendee_list.add(request.user)
    event.save()
    return JsonResponse({"message": f"You have successfully enrolled. Event: {event.name}"}, status=200)
