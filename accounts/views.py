import google.generativeai as genai
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.shortcuts import redirect
from django.views import View
from django.core.mail import send_mail
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decouple import config


from accounts.forms import LoginForm, SignupForm

genai.configure(api_key=config('GEMINI_API_KEY'))


class UserProfileSetupView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_setup.html'

    def post(self, request, *args, **kwargs):
        user = request.user

        if 'skip' in request.POST:
            user.profile_completed = False
            user.save()
            return redirect('home')


        full_name = request.POST.get('full_name')
        bio = request.POST.get('bio')
        skills = request.POST.get('skills')
        interests = request.POST.get('interests')
        avatar = request.FILES.get('avatar')

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

        return redirect('home')



class AccountHomeRedirectView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/auth/registration/profile-setup/')




class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_profile'] = self.request.user
        return context




def post(self, request, *args, **kwargs):
    user = request.user
    if 'skip' in request.POST:
        ...
        send_mail(
            'Welcome!',
            'You have successfully registered on Netxwork!',
            'netxwork@example.com',
            [user.email],
            fail_silently=True,
        )
        return redirect('home')
    ...
    send_mail(
        'Profile is complete!',
        'Your Netxwork profile has been successfully updated.',
        'netxwork@example.com',
        [user.email],
        fail_silently=True,
    )
    return redirect('home')





@csrf_exempt
def mentor_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question')

            model = genai.GenerativeModel('gemini-1.5-pro')

            response = model.generate_content(question)

            print("Gemini API SDK response:", response)

            return JsonResponse({'answer': response.text})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'answer': 'AI could not generate a response.'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
