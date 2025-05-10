import json

import google.generativeai as genai
import requests
from decouple import config
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login


from accounts.forms import LoginForm, SignupForm

from .models import User

genai.configure(api_key=config("GEMINI_API_KEY"))


class UserProfileSetupView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile_setup.html"

    def post(self, request, *args, **kwargs):
        user = request.user

        if "skip" in request.POST:
            user.profile_completed = False
            user.save()
            return redirect("dashboard")

        full_name = request.POST.get("full_name")
        bio = request.POST.get("bio")
        skills = request.POST.get("skills")
        interests = request.POST.get("interests")
        avatar = request.FILES.get("avatar")

        if full_name:
            user.full_name = full_name
        if bio:
            user.bio = bio
        if skills:
            user.skills = skills
        if interests:
            user.interests = interests
        if avatar:
            user.avatar = avatar

        user.profile_completed = True
        user.save()

        return redirect("dashboard")


class AccountHomeRedirectView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/auth/registration/profile-setup/")


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_profile"] = self.request.user
        return context


def post(self, request, *args, **kwargs):
    user = request.user
    if "skip" in request.POST:
        ...
        send_mail(
            "Welcome!",
            "You have successfully registered on Netxwork!",
            "netxwork@example.com",
            [user.email],
            fail_silently=True,
        )
        return redirect("home")
    ...
    send_mail(
        "Profile is complete!",
        "Your Netxwork profile has been successfully updated.",
        "netxwork@example.com",
        [user.email],
        fail_silently=True,
    )
    return redirect("home")


@csrf_exempt
def mentor_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question")

            model = genai.GenerativeModel("gemini-1.5-pro")

            response = model.generate_content(question)

            print("Gemini API SDK response:", response)

            return JsonResponse({"answer": response.text})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"answer": "AI could not generate a response."})

    return JsonResponse({"error": "Invalid request method"}, status=400)


def index_page(request):
    if request.method == "POST":
        # print('skibidi', request.POST.get("email"))
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, 'index.html', {'errors': ['Неверный логин или пароль']})
    else:
        return render(request, "index.html", {
            'login_form': LoginForm(),
            'signup_form': SignupForm()
        })


def filter_page(request) -> HttpResponse:
    return render(request, "filter.html")


def dashboard_page(request) -> HttpResponse:
    return render(request, "dashboard.html")


def check_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.profile_completed = True
        user.save()
        return render(request, 'account/email_confirm2.html')
    else:
        return HttpResponse('failed')


def email_confirmm(request):
    if request.method == "POST":
        errors = []
        password = request.POST.get("password2").strip()
        password2 = request.POST.get("password3").strip()
        full_name = request.POST.get("full_name").strip()
        email = request.POST.get("email2").strip()
        try:
            user = User.objects.get(email=email)
            errors.append('User with this email already exists.')
        except User.DoesNotExist:
            pass

        if password != password2:
            errors.append('Passwords do not match.')

        user = User.objects.create_user(email=email, password=password, username=full_name)
        if errors:
            for error in errors:
                messages.error(request, str(error))
            return redirect('/')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Ссылка подтверждения
        confirm_url = request.build_absolute_uri(
            reverse('check_email', kwargs={'uidb64': uid, 'token': token})
        )
        send_mail(
            subject='Confirm your email address',
            message=
            f'''
            Hi {full_name}!

            Thank you for signing up. Please confirm your email address by clicking the link below:
            
            {confirm_url}
            
            If you did not create an account, please ignore this email.
            
            Best regards,  
            The netXwork Team
            ''',
            from_email='noreply@example.com',  # адрес отправителя
            recipient_list=[email],  # список получателей
        )
        return render(request, "account/verification_sent_a.html")
