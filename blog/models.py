from typing import Text
from django.db import models
import datetime
from django.db.models.fields import IntegerField, TextField
from django.db.models.fields.related import ForeignKey
import django.utils.timezone as tm
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    ONLY_ME = 'ONLY_ME'
    FRIENDS = 'FRIENDS'
    PUBLIC = 'PUBLIC'
    VISIBILITY = [
        ( ONLY_ME,"Only Me"),
        (FRIENDS,"Friends"),
        (PUBLIC,"Public")
    ]
    id = IntegerField(primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogs')
    content = models.TextField()
    subject = models.TextField()
    votes = models.IntegerField(default=0)
    visibility = models.CharField(
        choices=VISIBILITY,
        default = ONLY_ME,
        max_length=20
    )
    date_posted = models.DateTimeField(default=tm.now)
    upvoted = models.ManyToManyField(User,related_name='upvoted_blogs',blank=True)
    downvoted = models.ManyToManyField(User,related_name='downvoted_blogs',blank=True)
    class Meta():
        ordering = ['-date_posted']
    def __str__(self):
        return self.subject
    def get_voted(self):
        return self.votes
    def get_content(self):
        return self.content
    def get_subject(self):
        return self.subject
    def get_date_posted(self):
        return self.date_posted
    def upvote(self,usr):
        if usr in self.upvoted.all():
            self.author.profile.rating-=1            
            self.votes-=1            
            self.upvoted.remove(usr)            
        else:
            if usr in self.downvoted.all():
                self.author.profile.rating+=1                
                self.votes+=1                
                self.downvoted.remove(usr)
            self.author.profile.rating+=1
            self.votes+=1
            self.upvoted.add(usr)
        self.author.profile.save()
        self.save()
    def downvote(self,usr): 
        if usr in self.downvoted.all():
            self.author.profile.rating+=1
            self.votes+=1
            self.downvoted.remove(usr)  
        else:
            if usr in self.upvoted.all():
                self.author.profile.rating-=1
                self.votes-=1
                self.upvoted.remove(usr)
            self.author.profile.rating-=1
            self.votes-=1
            self.downvoted.add(usr)
        self.author.profile.save()
        self.save()
    def is_only_me(self):
        return self.visibility is self.ONLY_ME
    def is_public(self):
        return self.visibility is self.PUBLIC
    def is_friends(self):
        return self.visibility is self.FRIENDS



class Comment(models.Model):
    id = IntegerField(primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    subject = TextField()
    content = TextField()
    blog_ref = ForeignKey(Blog,related_name='comments',on_delete=models.CASCADE)
    votes = IntegerField(default=0)
    upvoted = models.ManyToManyField(User,related_name='upvoted_comments',blank=True)
    downvoted = models.ManyToManyField(User,related_name='downvoted_comments',blank=True)
    date_posted = models.DateTimeField(default=tm.now)
    class Meta():
        ordering = ['-date_posted']
    def __str__(self):
        return self.subject

    def upvote(self,usr):
        if usr in self.upvoted.all():
            self.author.profile.rating-=1            
            self.votes-=1            
            self.upvoted.remove(usr)            
        else:
            if usr in self.downvoted.all():
                self.author.profile.rating+=1                
                self.votes+=1                
                self.downvoted.remove(usr)
            self.author.profile.rating+=1
            self.votes+=1
            self.upvoted.add(usr)
        self.author.profile.save()
        self.save()
    def downvote(self,usr):
        if usr in self.downvoted.all():
            self.author.profile.rating+=1
            self.votes+=1
            self.downvoted.remove(usr)  
        else:
            if usr in self.upvoted.all():
                self.author.profile.rating-=1
                self.votes-=1
                self.upvoted.remove(usr)
            self.author.profile.rating-=1
            self.votes-=1
            self.downvoted.add(usr)
        self.author.profile.save()
        self.save()