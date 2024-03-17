from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from Election import *
from django.urls import reverse

# Create your views here.

def home(request):
    """Render the home page."""
    return render(request, "base.html")

def login_page(request):
    """Handle user login."""
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        if not User.objects.filter(username=user_name).exists():
            messages.error(request, "Invalid User Name")
            return redirect(reverse("login_page"))

        user = authenticate(username=user_name, password=password)
        if user is None:
            messages.error(request, "Invalid Password")
        else:
            login(request, user)
            return redirect("/home_prediction/")

    return render(request, "login.html")

def register_page(request):
    """Handle user registration."""
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        if User.objects.filter(username=user_name).exists():
            messages.info(request, "User already exists with this name")
            return redirect("/register/")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=user_name
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account Created Successfully")
        return redirect("/register/")

    return render(request, "register.html")

def log_out_page(request):
    """Handle user logout."""
    logout(request)
    return redirect("/login/")

def home_prediction(request):
    """Render the prediction home page."""
    return render(request, "prediction.html")

def prediction(request):
    """Handle election predictions."""
    if request.method == "POST":
        state = request.POST.get("state")
        INDIA = request.POST.getlist("INDIA")
        NDA = request.POST.getlist("NDA")

        if state == "Choose...":
            messages.info(request, "State has not been selected")
            return redirect("/prediction/")
        else:
            df1 = pd.read_csv("Election/ALL_STATE.csv")
            df1.fillna(0, inplace=True)
            swing = df1.loc[df1["State"] == state]

            election_state = "Election\\" + state + ".csv"
            df = pd.read_csv(election_state, encoding="windows-1252")
            df['NDA'] = 0
            df['INDIA'] = 0
            df.fillna(0, inplace=True)

            for b in NDA:
                if b in df.columns:
                    t = int(swing.loc[:, b].values)
                    df['NDA'] = df['NDA'] + df[b] + ((df[b] * (t)) / 100)
            for a in INDIA:
                if a in df.columns:
                    t = int(swing.loc[:, a].values)
                    df["INDIA"] = df["INDIA"] + df[a] + ((df[a] * (t)) / 100)

            INDIA = 0
            NDA = 0
            for index, row in df.iterrows():
                if row['INDIA'] > row['NDA']:
                    INDIA += 1
                else:
                    NDA += 1

            messages.info(request, "State has been selected")
            return render(request, "result.html", {"d": [NDA, INDIA], "n": ["NDA", "INDIA"], "state": state})

    return render(request, "prediction.html")
