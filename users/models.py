from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(blank=True)
    pic = models.ImageField(default="default.png",blank=True)    
    rating = models.IntegerField(default=0)
    friends = models.ManyToManyField('self',related_name='friend_list',blank=True,symmetrical=True)    
    friend_req_list = models.ManyToManyField('self',related_name='friend_req_lst',blank=True,symmetrical=False)
    class Meta:
        ordering = ['-rating']
    def __str__(self) :
        return self.user.username
    def send_friend_req(self,frnd):        
        if self not in frnd.profile.friend_req_list.all(): frnd.profile.friend_req_list.add(self)
    def accept_friend_req(self,frnd):
        try:
            self.friend_req_list.remove(frnd.profile)
            self.friends.add(frnd.profile)
        except Exception as e:
            print(str(e))



    


    










