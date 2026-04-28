from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        password_confirm = request.POST.get("password_confirm", "").strip()

        if not username or not password or not password_confirm:
            return render(request, "accounts/signup.html", {"error": "모든 값을 입력하세요."})

        if password != password_confirm:
            return render(request, "accounts/signup.html", {"error": "비밀번호가 일치하지 않습니다."})

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {"error": "이미 존재하는 아이디입니다."})

        User.objects.create_user(username=username, password=password)
        return redirect("accounts:login")

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")  # smartcs home

        return render(request, "accounts/login.html", {"error": "로그인 실패"})

    return render(request, "accounts/login.html")