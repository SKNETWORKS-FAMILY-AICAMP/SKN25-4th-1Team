from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        password_confirm = request.POST.get("password_confirm", "").strip()

        if not username or not password or not password_confirm:
            return render(request, "accounts/signup.html", {
                "error": "모든 항목을 입력해주세요."
            })

        if password != password_confirm:
            return render(request, "accounts/signup.html", {
                "error": "비밀번호가 일치하지 않습니다."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "이미 존재하는 아이디입니다."
            })

        User.objects.create_user(username=username, password=password)

        return render(request, "accounts/signup.html", {
            "success": "회원가입이 완료되었습니다. 로그인해주세요."
        })

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            return render(request, "accounts/login.html", {
                "error": "아이디와 비밀번호를 입력해주세요."
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("로그인 성공:", request.user)
            return redirect("/")

        return render(request, "accounts/login.html", {
            "error": "아이디 또는 비밀번호가 올바르지 않습니다."
        })

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")