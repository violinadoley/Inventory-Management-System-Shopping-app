
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django01 import settings
from django.core.mail import send_mail, EmailMessage
from page1.models import BookIssue, BookPublish, BookReview, Author
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token


# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def author(request):
    authorname=""
    authorID=""
    authoremail=""
    no_of_works=""
    if request.method == "POST":
        # Process the form data here
        authorname = request.POST.get('authorname')
        print(authorname)
        authorID = request.POST.get('authorID')
        print(authorID)
        authoremail = request.POST.get('authoremail')
        print(authoremail)
        no_of_works = request.POST.get('no_of_works')
        print(no_of_works)

        # Save the form data to the Author model or perform any other necessary actions
        # For example:
        author = Author(authorname=authorname, authorID=authorID, authoremail=authoremail, no_of_works=no_of_works)
        author.save()

    return render(request, 'author.html', {'authorname': authorname, 'authorID': authorID, 'authoremail': authoremail, 'no_of_works': no_of_works})


def issuebooks(request):
    if request.method == "POST":
        booktitle = request.POST.get('booktitle')
        authorname = request.POST.get('authorname')
        ISBN = request.POST.get('ISBN')

        issue = BookIssue(booktitle=booktitle, authorname=authorname,ISBN=ISBN, date=datetime.today())
        issue.save()
    return render(request, 'issuebooks.html')


def landing(request):
    return render(request, 'landing.html')


def publishbook(request):
    if request.method == "POST":
        booktitle = request.POST.get('booktitle')
        authorname = request.POST.get('authorname')
        ISBN = request.POST.get('ISBN')
        desc = request.POST.get('desc')

        publ = BookPublish(booktitle=booktitle, authorname=authorname,desc=desc, ISBN=ISBN, publdate=datetime.today())
        publ.save()

        # success_message = "Your book has been published successfully!"
        # return render(request, 'publishbook.html',{'success_message': success_message})
    return render(request, 'publishbook.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(username, email, password)
        myuser.username = username
        # myuser.is_active = False
        myuser.save()

        # if User.objects.filter(username = username):
        #     messages.error(request, "Username already exists!")
        #     return redirect('register.html')

        # if User.objects.filter(email=email):
        #     messages.error(request, "Email already registered!")
        #     return redirect('register.html')

        # if username.isalnum():
        #     messages.error(request,"Username must be alphanumeric")
        #     return redirect('register.html')

        # messages.success(request,"Account successfully created!")

        # subject = "Welcome to BP\n"
        # message = "Thanku for signing up\n\n"
        # from_email =  settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject,message,from_email,to_list, fail_silently=True)

        # current_site = get_current_site(request)
        # email_subject = "Confirm Email"
        # message2 = render_to_string('email_configuration.html',{
        #     'name':myuser.username,
        #     'domain':current_site.domain,
        #     'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
        #     'token': generate_token.make_token(myuser)
        #       })

        # email = EmailMessage(
        #     email_subject,
        #     message2,
        #     settings.EMAIL_HOST_USER,
        #     [myuser.email],
        # )
        # email.fail_silently = True
        # email.send()

        return redirect('signin')
    return render(request, 'register.html')


def returnbook(request):
    
    return render(request, 'returnbook.html')

def wishlisted(request):
    return render(request, 'wishlisted.html')

def review(request):
    booktitle = ""
    review = ""
    if request.method == "POST":
        name = request.POST.get('name')
        print(name)
        booktitle = request.POST.get('booktitle')
        print(booktitle)
        review = request.POST.get('review')
        print(review)
        rev = BookReview(name=name, booktitle=booktitle, review=review, date=datetime.today())
        rev.save()
      
       # return HttpResponse("Review Added!")
    return render(request, 'review.html', {'booktitle': booktitle, 'review': review})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            username = user.username
            return render(request, 'userdashboard.html', {'username': username})
        else:
            messages.error(request, "User not signed up")
            return redirect('signin')

    return render(request, 'signin.html')


def userdashboard(request):

    return render(request, 'userdashboard.html')


# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         myuser = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         myuser = None

#     if myuser is not None and generate_token.check_token(myuser, token):
#         myuser.is_active = True
#         myuser.save()
#         login(request, myuser)
#         return render(request, 'userdashboard.html', {'name' : username})
#     else:
#         return render(request, 'activation_failed.html')
