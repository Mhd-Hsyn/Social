from django.db import models
import uuid
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,max_length=255)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    # def __str__(self):
    #     return self.id
    


class Users(BaseModel):
    fname = models.CharField( max_length=50)
    lname = models.CharField( max_length=50)
    email = models.EmailField( max_length=254, unique= True)
    password = models.TextField()
    username = models.CharField( max_length=50, unique=True)
    profile = models.ImageField(upload_to="my_picture", blank=True, default="user_default/default_img.png")
    
    def __str__(self):
        return self.username
    

class UserPost(BaseModel):        
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    image = models.ImageField( upload_to="post_picture", height_field=None, width_field=None, max_length=None, default=None)
    caption = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Likes(BaseModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

class Comment(BaseModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)    
        
    