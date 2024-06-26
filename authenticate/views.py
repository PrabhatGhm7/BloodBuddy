from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string 
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from . tokens import generate_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import UserProfile
import mysql.connector
def home(request):
    return render(request, 'index.html')

def signup(request):
    # Signup form
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        bloodgroup = request.POST.get("bloodgroup")
        age = request.POST.get("age")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        

        # Validate username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try a different username.")
            return redirect('home')

        # Validate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('home')

        # Validate password
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')

        reqage = int(age)
        if reqage < 18:
            messages.error(request, "You need to be at least 18 years old")
            return redirect('home')

        # Create user object
        myuser = User.objects.create_user(username, email, pass1)
        myuser.is_active = False
        myuser.save()
        
                         
                    

        # Create UserProfile associate with the User and them adding it to myuser
        UserProfile.objects.create(user=myuser, fullname=fullname, age=age, gender=gender, bloodgroup=bloodgroup, address=address)
        
        # Send welcome email
        subject = "Welcome to Blood Buddy"
        message = f"Hello {myuser.first_name}!\n\n Please confirm your email address to activate your account.\n\nRegards,\nThe Blood Buddy Team"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [myuser.email], fail_silently=True)

        # Send email confirmation link
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email Address"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)

        })
        email = EmailMessage(
            email_subject,
            message2,
            from_email=settings.EMAIL_HOST_USER,
            to=[myuser.email],
        )
        email.send()
        

        messages.success(request, "Your account has been created successfully! Please check your email to activate your account.")
        return redirect('signin')
    
    return render(request, "signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')




def signin(request, signup=None):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        # Authentication successful
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Successfully signed in!')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
        
    return render(request, 'signin.html')


#main profile page
def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in first')
        return redirect('home')
    print(request.session.items())
    current_username = request.user.username
    user_profile = UserProfile.objects.get(user=request.user)
    
    return render(request, 'profile.html', {'user_profile': user_profile, 'current_username': current_username})
        
def search(request):
    
    #for searching in search
    if request.method == 'POST':
        srch_bloodgroup = request.POST.get('bloodgroup')
        srch_address = request.POST.get('address')
        person = UserProfile.objects.filter(bloodgroup__icontains=srch_bloodgroup, address__icontains=srch_address)
        return render(request,'search.html',{'person':person})

    return render(request, 'search.html')
    

#logout page
def signout(request):
    logout(request)
    messages.success(request, 'Log out successfully')
    return redirect('home')
