from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
import datetime
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Blog,Comment
# Create your views here.


@login_required
def post_blog(request):
    try:
        if(request.method == 'POST'):
            blg = Blog.objects.create(
                author=request.user,
                subject=request.POST['subject'],
                content=request.POST['content'],
                visibility = request.POST['visibility']
            )
            blg.save()
            return redirect(request.META['HTTP_REFERER'])

    except Exception :
        return HttpResponse('Failed To post Blog')

@login_required
def update_blog(request,**kwargs):
    try:
        if(request.method == 'POST'):
            blg_id = kwargs.get('blog_id')
            if(blg_id is None):
                return HttpResponseNotFound('Page Not Found')
            blg = Blog.objects.get(id = blg_id)
            if blg is None:
                return HttpResponseNotFound('Blog does not exist')
            if(request.user != blg.author):
                return HttpResponseForbidden('You dont have right to edit others blogs')            
            blg.subject = request.POST['subject']
            blg.content = request.POST['content']
            blg.visibility = request.POST['visibility']
            blg.save()
            return redirect(request.META['HTTP_REFERER'])

    except Exception :
        return HttpResponse('Failed To post Blog')
@login_required
def upvote(request,**kwargs):
    if(request.method=='POST'):
        curr_blg = Blog.objects.get(id=kwargs['blog_id'])
        curr_blg.upvote(request.user)
        return redirect(request.META['HTTP_REFERER'])

@login_required
def downvote(request,**kwargs):
    if(request.method=='POST'):
        curr_blg = Blog.objects.get(id=kwargs['blog_id'])
        curr_blg.downvote(request.user)
        return redirect(request.META['HTTP_REFERER'])

@login_required
def add_comment(request,**kwargs):
    if(request.method=='POST'):
        curr_blg = Blog.objects.get(id=kwargs['blog_id'])
        comment = Comment(
            author = request.user,
            subject = request.POST['subject'],
            content = request.POST['content'],
            blog_ref = curr_blg)
        comment.save()
        return redirect(request.META['HTTP_REFERER'])

@login_required
def upvote_comment(request,**kwargs):
    if(request.method=='POST'):
        curr_cmt = Comment.objects.get(id = kwargs['comment_id'])
        curr_cmt.upvote(request.user)
        return redirect(request.META['HTTP_REFERER'])

@login_required
def downvote_comment(request,**kwargs):
    if(request.method=='POST'):
        curr_cmt = Comment.objects.get(id = kwargs['comment_id'])
        curr_cmt.downvote(request.user)
        return redirect(request.META['HTTP_REFERER'])

@login_required
def delete_blog(request):    
    curr_blg = Blog.objects.get(request.POST['blg_id'])
    curr_blg.delete()

@login_required
def get_blogs(request):
    if(request.method=='GET'):
        blg_list = []
        for blg in Blog.objects.all():
            if blg.is_public():
                blg_list.append(blg)
            elif blg.is_friends():
                if blg.author in request.user.profile.friends:
                    blg_list.append(blg)        
        return JsonResponse({'blg_list':blg_list})

        