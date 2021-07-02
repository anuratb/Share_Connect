from rest_framework import generics
import json
from .serializers import ProfileSerializer
from .models import Profile
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from blog.models import Blog
from .forms import ImageForm
from .forms import PasswordForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

a = HttpRequest()

# Create your views here.


class ProfileListCreate(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


def home(request):
    if(request.user.is_authenticated):
        return render(request, 'home.html', {'user': request.user.profile, 'is_auth': True})
    else:
        return render(request, 'home.html', {'is_auth': False})


@login_required
def update_profile(request):
    if(request.method == 'GET'):
        form = ImageForm(empty_permitted=True,use_required_attribute=False)
        return render(request, 'update_profile.html', {"user": request.user.profile, "form": form, "alert_success": False})
    elif request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if(form.is_valid()):
            print(form.cleaned_data['pic'])
            if form.cleaned_data['pic'] is not None : request.user.profile.pic = form.cleaned_data['pic']
        else:
            print('Invalid')
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.email = request.POST['email']
        request.user.save()
        request.user.profile.bio = request.POST['bio']
        request.user.profile.bio = request.POST['bio']
        request.user.profile.save()
        return render(request, 'update_profile.html', {"user": request.user.profile, "form": ImageForm(), "alert_success": True})

def blogs(request,**kwargs):
    if request.method=='GET':
        if(kwargs.get('username') is None):            
            blgs = []
            is_auth = request.user.is_authenticated
            if is_auth:
                
                for blg in Blog.objects.all():                    
                    if blg.visibility == Blog.PUBLIC:                        
                        blgs.append(blg)
                    elif blg.visibility == Blog.FRIENDS and request.user.profile in blg.author.profile.friends.all() :                        
                        blgs.append(blg)
                    elif (blg.visibility == Blog.ONLY_ME or blg.visibility == Blog.FRIENDS) and (request.user.username == blg.author.username):                        
                        blgs.append(blg)
                
                return render(request,'blogs.html',{                
                    'blgs':[{'blg':blg,'comments':[{
                            'comment':comment,
                            'upvoted':request.user in comment.upvoted.all(),
                            'downvoted':request.user in comment.downvoted.all()
                            }for comment in blg.comments.all()],
                    'upvoted':request.user in blg.upvoted.all(),
                    'downvoted':request.user in blg.downvoted.all()} for blg in blgs],
                    'is_auth': is_auth,
                    'curr_user':request.user.profile
                })
            else :
                blgs = Blog.objects.filter(visibility=Blog.PUBLIC)
                print(blgs)
                return render(request,'blogs.html',{                
                    'blgs':[{'blg':blg,'comments':[{
                            'comment':comment
                            }for comment in blg.comments.all()]} for blg in blgs],
                    'is_auth': is_auth
                })
        usr = User.objects.get(username=kwargs['username'])
        is_auth = request.user.is_authenticated
        if usr is not None:
            if is_auth:
                if usr == request.user:
                    blgs = usr.blogs.all()
                else:
                    is_friend = len(usr.profile.friends.filter(user=request.user)) >0
                    blgs = usr.blogs.filter(Q(visibility=Blog.PUBLIC)|Q(visibility=Blog.FRIENDS)) if is_friend else usr.blogs.filter(Q(visibility=Blog.PUBLIC)|Q(visibility=Blog.FRIENDS))
                return render(request,'blogs.html',{
                'user' : usr.profile,
                'blgs':[{'blg':blg,'comments':[{
                            'comment':comment,
                            'upvoted':request.user in comment.upvoted.all(),
                            'downvoted':request.user in comment.downvoted.all()
                            }for comment in blg.comments.all()],
                    'upvoted':request.user in blg.upvoted.all(),
                    'downvoted':request.user in blg.downvoted.all()} for blg in blgs],
                'is_auth': is_auth,
                'curr_user':request.user.profile
            })
            else:
                blgs = usr.blogs.filter(visibility=Blog.PUBLIC)
                return render(request,'fblogs.html',{
                'user' : usr.profile,
                'blgs':[{'blg':blg,'comments':[{
                            'comment':comment
                            }for comment in blg.comments.all()]} for blg in blgs],
                'is_auth': is_auth
            })
            
        else:
            return HttpResponseNotFound('The username '+kwargs['username']+' does not exits')
    
def friends(request, **kwargs):
    if request.method == 'GET':
        usr = User.objects.get(username=kwargs['username'])
        is_auth = request.user.is_authenticated
        if usr is not None:
            if is_auth:
                return render(request,'friends.html',{
                'user' : usr.profile,
                'friends': usr.profile.friends.all(),
                'is_auth': is_auth,
                'curr_user':request.user.profile
            })
            else:
                return render(request,'friends.html',{
                'user' : usr.profile,
                'friends': usr.profile.friends.all(),
                'is_auth': is_auth
            })
            
        else:
            return HttpResponseNotFound('The username '+kwargs['username']+' does not exits')

@login_required
def friend_requests(request):
    if request.method == 'GET':
        usr = request.user
        
        return render(request,'friend_requests.html',{                
                'friend_requests': usr.profile.friend_req_list.all(),
                'is_auth': True,
                'curr_user':request.user.profile
            })

def search(request):
    if request.method == 'POST':
        src_text = request.POST['src_text']        
        is_auth = request.user.is_authenticated
        src_results = []
        for usr in User.objects.all():
            if src_text.lower() in str(usr.username).lower():
                src_results.append(usr.profile)
            elif src_text.lower() in str(usr.first_name).lower():
                src_results.append(usr.profile)
            elif src_text.lower() in str(usr.last_name).lower():
                src_results.append(usr.profile)
            elif src_text.lower() in str(str(usr.first_name)+' '+str(usr.last_name)).lower():
                src_results.append(usr.profile)
        if is_auth:
            
            return render(request,'search.html',{            
            'src_results':src_results,
            'is_auth': is_auth,
            'curr_user':request.user.profile
        })
        else:
            return render(request,'search.html',{            
            'src_results':src_results,
            'is_auth': is_auth
        })

def profile(request, **kwargs):
    if(request.method == 'GET'):
        if len(User.objects.filter(username=kwargs['username'])) == 0:
            return HttpResponseNotFound('User does not Exist')
        if(request.user.is_authenticated):

            if(kwargs['username'] == request.user.username):
                # current user
                blgs = request.user.blogs.all()  # Get all blogs

                return render(request, 'profile.html', {
                    "user": request.user.profile,
                    "is_curr_user": True,
                    "nf": request.user.profile.friends.count(),
                    "is_auth": True,
                    'blgs':[{'blg':blg,'comments':[{
                            'comment':comment,
                            'upvoted':request.user in comment.upvoted.all(),
                            'downvoted':request.user in comment.downvoted.all()
                            }for comment in blg.comments.all()],
                    'upvoted':request.user in blg.upvoted.all(),
                    'downvoted':request.user in blg.downvoted.all()} for blg in blgs],
                    'curr_user':request.user.profile
                })
            else:
                # others view
                usr = User.objects.get(username=kwargs['username'])
                is_friend = len(usr.profile.friends.filter(
                    user=request.user)) > 0
                # get friends and public blogs
                blgs = usr.blogs.filter(Q(visibility=Blog.PUBLIC) | Q(
                    visibility=Blog.FRIENDS)) if is_friend else usr.blogs.filter(visibility=Blog.PUBLIC)
                return render(request, 'profile.html', {
                    "user": usr.profile,
                    "is_curr_user": False,
                    "nf": usr.profile.friends.count(),
                    "is_auth": True,
                    "is_friend": is_friend,
                    "friend_req_sent": usr.profile in request.user.profile.sent_friend_req_list.all(),
                    'blgs':[{'blg':blg,'comments':[{
                            'comment':comment,
                            'upvoted':request.user in comment.upvoted.all(),
                            'downvoted':request.user in comment.downvoted.all()
                            }for comment in blg.comments.all()],
                    'upvoted':request.user in blg.upvoted.all(),
                    'downvoted':request.user in blg.downvoted.all()} for blg in blgs],
                    'curr_user':request.user.profile
                })
        else:
            # Public View
            usr = User.objects.get(username=kwargs['username'])
            # get public blogs
            blgs = usr.blogs.filter(visibility=Blog.PUBLIC)
            return render(request, 'profile.html', {
                "user": usr.profile,
                "is_curr_user": False,
                "nf": usr.profile.friends.count(),
                "is_auth": False,
                'blgs':[{'blg':blg,'comments':[{
                            'comment':comment
                            }for comment in blg.comments.all()]} for blg in blgs]
            })


def handleLogin(request):
    #print('Handling Login')
    '''
    reequest has fields 'username ' and 'password'

    '''
    if(request.user.is_authenticated):
        return redirect('/users/home')
    if request.method == 'POST':
        usr = auth.authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if usr is None:
            return render(request, 'login.html', {'wrong_cred': True})
        else:
            auth.login(request, usr)
            return redirect('/users/home')
    elif request.method == 'GET':
        return render(request, 'login.html', {'wrong_cred': False})


def handleSignUp(request):
    # Function for signing up new users
    if request.user.is_authenticated:
        return redirect('/users/home')
    if(request.method == 'POST'):
        usr_name = request.POST['username']
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
        else:
            return render(request, 'sign_up.html', {'password_invalid': True})
        print(password)
        if len(User.objects.filter(username=usr_name)) > 0:
            return render(request, 'sign_up.html', {'username_exists': True})
        else:
            usr = User.objects.create_user(username=usr_name,
                       password=password,
                       first_name=request.POST['first_name'],
                       last_name=request.POST['last_name'],
                       email=request.POST['email']
                       )
            
            profile = Profile(user=usr, bio="", rating=0)
            profile.save()
            return redirect('/users/home')
    elif request.method == 'GET':
        form = PasswordForm()
        return render(request, 'sign_up.html',{'password_form':form})


'''
def forgot_pass(request):
    if request.method=='GET':
        return render(request,'forgot.html')
    elif request.method=='POST':
        email_data = request.POST['email']
        usrs = User.objects.filter(email=email_data)
        if(len(usrs)>0):
            for usr in usrs:
                subject = "Reset Password"
                options = {
                    "email":usr.email,
                    "domain":"http://127.0.0.1:8000",
                    "site_name":"Share and Connet",
                    "uid" : urlsafe_base64_encode(force_bytes(usr.pk)),
                    "user": usr,
                    "token":default_token_generator.make_token(usr),
                    "protocol":"http"
                }
                email = render_to_string('email.txt',options)
                try:
                    send_mail(subject,email,from_email='anuratb@yahoo.com' ,recipient_list=[usr.email],fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid Header')

        return render(request,'reset_conf.html')
'''


def isLoggedIn(request):
    if(request.user.is_authenticated):
        return JsonResponse({'logged_in': True})
    else:
        return JsonResponse({'logged_in': False})


@login_required()
def logout(request):
    try:
        auth.logout(request)
        return render(request, 'logout.html')
    except:
        return JsonResponse({'status': False, 'message': 'Some errorr occured'})


@login_required
def accept_request(request,**kwargs):
    if request.method=='POST':
        usr = User.objects.get(username=kwargs['username'])
        if usr is None:
            return HttpResponseNotFound('Usnername doesnt exist ')
        if request.user.profile.friend_req_list.get(user=usr) is not None:
            request.user.profile.friend_req_list.remove(usr.profile)
            request.user.profile.friends.add(usr.profile)
            request.user.profile.save()
            usr.profile.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseNotFound('Username '+kwargs['username']+' doesnt exist in your friend request list')

@login_required
def reject_request(request,**kwargs):
    if request.method=='POST':
        usr = User.objects.get(username=kwargs['username'])
        if usr is None:
            return HttpResponseNotFound('Usnername doesnt exist ')
        if request.user.profile.friend_req_list.get(user=usr) is not None:
            request.user.profile.friend_req_list.remove(usr.profile)            
            request.user.profile.save()
            usr.profile.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseNotFound('Username '+kwargs['username']+' doesnt exist in your friend request list')
@login_required
def send_friend_request(request,**kwargs):
    if request.method=='POST':
        usr = User.objects.get(username=kwargs['username'])#to send req to usr from curr_user
        if usr is None:
            return JsonResponse({
                'status' : False,
                'msg':'Username Doesnt exist'
            })
        if usr.profile not in request.user.profile.friends.all():
            if usr.profile not in request.user.profile.sent_friend_req_list.all():
                #send friend request
                usr.profile.friend_req_list.add(request.user.profile)                
                request.user.profile.save()
                usr.profile.save()
                return JsonResponse({
                    'status' : True
                })
            else:
                #cancel friend request
                usr.profile.friend_req_list.remove(request.user.profile)
                request.user.profile.save()
                usr.profile.save()
                return JsonResponse({
                    'status' : True
                })
        else:
            return JsonResponse({
                    'status' : False,
                    'msg' : 'User is already the friend'
                })
