from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import Useable.useable as uc
from Useable.permission import userauthorization
from operator import itemgetter
import jwt
from passlib.hash import django_pbkdf2_sha256 as handler
import Useable.emailpattern as verfied
import random 
#########################
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decouple import config
import requests


# Create your views here.


class UserSignupView(APIView):
    def post(self, request):
        try:
            serializer = AddUserSerializer(data= request.data)
            if not serializer.is_valid():
                return Response ({"status" : "False", "error":serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({"status": "True", "message": "Signup Successfully !!!"}, status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"status": "False", "error": str(e)}, status.HTTP_404_NOT_FOUND)




class UserLoginView(APIView):
    def post (self, request):
        
        data = request.data
        username = request.data.get('username')
        password = request.data.get('password')
        
        serializer = UserLoginSerializer(data= request.data)
        if serializer.is_valid():
            if "@" in data.get('username'):
                fetchuser = Users.objects.filter(email = username).first()
            
            else:
                fetchuser = Users.objects.filter(username = username).first()
            
            if fetchuser and handler.verify(password, fetchuser.password):
                authkey = "abcd@123"
                token = uc.usergeneratedToken(fetchuser= fetchuser,authKey= authkey, request=request, totaldays= 1 )
                
                # jwtkeys = {"user": config("userjwttoken")}
                # generate_auth = uc.usergeneratedToken(fetchuser, jwtkeys['user'], 1, request)
                
                print (token)
                return Response({"msg": "Login Successfully", "token": token['token'], "data": token['payload']})
            
            else:
                return Response({"error": "invalid credentials . . . "})
            
        return Response({"error": serializer.errors})
    
    

class userprofile(APIView):
    permission_classes = [userauthorization]

    def get(self, request):
        try:
            fetchuser = Users.objects.filter(
                id=request.GET['token']['id']).first()
            
            # print(fetchuser)
            # print(str(fetchuser.id))
            
            access_token_payload = {
                "id": fetchuser.id,
                "fname": fetchuser.fname,
                "lname": fetchuser.lname,
                "email": fetchuser.email,
                "username":fetchuser.username,
                "profile": fetchuser.profile.url
                # "address": fetchuser.address,
                # "contact": fetchuser.contact
            }

            return Response({"status": True, "data": access_token_payload})

        except Exception as e:
            message = {'status': False}
            # message.update(message=str(e))if settings.DEBUG else message.update(
            #     message='Internal server error')
            return Response(message, status=500)    


    
    
    def put(self, request):
        try:
            
            fetchuser = Users.objects.filter(id=request.GET['token']['id']).first()
            
            fetchuser.fname, fetchuser.lname= itemgetter('fname', 'lname') (request.data)
            
            # if image come 
            
            if request.FILES.get('profile', False):
                fetchuser.profile = request.FILES['profile']

            fetchuser.save()
            # obj = uc.makedict(fetchuser, [
            #                     'id', 'fname', 'lname', 'address', 'contact', 'email', 'profile'], True)
            
            obj = {"id":str(fetchuser.id), "fname":fetchuser.fname, "lname":fetchuser.lname, "email":fetchuser.email, "username":fetchuser.username,"profile": fetchuser.profile.url ,
                   "token encode": jwt.encode( request.GET['token'], "abcd@123", algorithm='HS256'),
                   "token decoded": request.GET['token']}
            
            return Response({"status": True, "message": "Update Successfully", "data": obj})


        except Exception as e:
            message = {'status': False}
            return Response(message, status=500)
        







class userchangepassword(APIView):
    permission_classes = [userauthorization]

    def post(self, request):
        try:
            # requireFields = ['oldpassword', 'password']
            # print(request.GET['token']['id'])
            
            fetchuser = Users.objects.filter(id=request.GET['token']['id']).first()
            
            if handler.verify(request.data['oldpassword'], fetchuser.password):
                # check if user again use old password
                if not handler.verify(request.data['password'], fetchuser.password):

                    # password length validation
                    
                    if len(request.data['password']) < 8:
                        return Response({"status": False, "message": "Password must be 8 or less than 20 characters"})

                    fetchuser.password = handler.hash(request.data['password'])
                    fetchuser.save()

                    # black list token
                    # uc.userblacklisttoken(
                    #     request.GET['token']['id'], request.META['HTTP_AUTHORIZATION'][7:])

                    # Create new token
                    # jwtkeys = {"user": config("userjwttoken")}
                    jwtkeys = "abcd@123"
                    # generate_auth = uc.usergeneratedToken(fetchuser, jwtkeys["user"], 1, request)
                    generate_auth = uc.usergeneratedToken(fetchuser, jwtkeys, 1, request)
                    return Response({'status': True, 'message': 'Password Update Successfully', 'token': generate_auth['token']})

                else:
                    return Response({'status': False, 'message': 'You choose old password try another one'})

            else:
                return Response({'status': False, 'message': 'Your Old Password is Wrong'})

        except Exception as e:
            message = {'status': False}
            return Response(message, status=500)
        
        

class userforgotPasswordlinkSend(APIView):
    def post(self, request):
           
        email = request.data['email']
        
        fetchuser = Users.objects.filter(email=email).first()

        if fetchuser:
            # if fetchuser.status:
                token = random.randrange(1000, 100000, 5)
                # fetchuser.Otp = token
                # fetchuser.OtpCount = 0
                # fetchuser.OtpStatus = True
                # fetchuser.save()
                emailstatus = verfied.forgetEmailPattern({"subject": "forget password", "EMAIL_HOST_USER": config(
                    'EMAIL_HOST_USER'), "toemail": email, "token": token})
                if emailstatus:
                    return Response({'status': True, 'message': "Email send successfully", 'id': fetchuser.id})

                else:
                    return Response({'status': False, 'message': 'Something went wrong'})

            # else:
            #     return Response({'status': False, 'message': 'Your Account is disable'})

        else:
            return Response({'status': False, 'message': 'Email doesnot exist'})
    
    





class map(APIView):

    def get(self, request):
        # try:

        latitude = request.GET['latitude']
        longitude = request.GET['longitude']
        radius = request.GET['radius']  # in meters
        keyword = 'veterinary+clinic'    # veterinary_care   # veterinary+clinic
        key = config("key")

        response = requests.get(
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&keyword={keyword}&key={key}")

        data = response.json()

        return Response({'status': True, 'data': data})
  
  
  
  
  
  
  #############################      Social Post      ###########################
  
  
class UserPostView(APIView):
    permission_classes = [userauthorization]
    def post(self, request):
        id=request.GET['token']['id']
        # image = request.FILES.get('image')
        caption = request.data.get('caption') 
        
        fetchuser = Users.objects.filter(id = id).first()
        user_post = UserPost.objects.create(
            user = fetchuser, caption = caption)
        
        if request.FILES.get('image', False):
                user_post.image = request.FILES['image']
        
        user_post.save()
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "social",
            {
                'type': 'chat_message',
            }
        )   
        return Response({"msg": "Created !!!"})        
    
    
    def get(self, request):
        id=request.GET['token']['id']
        fetchuser = Users.objects.filter(id = id).first()
        user_posts = UserPost.objects.filter(user=fetchuser).order_by('-time')
        
        serialized_posts = []  # List to store serialized post data
        
        for post in user_posts:
            serialized_posts.append({
                "image": post.image.url if post.image else None,
                "caption": post.caption,
                "time": post.time,
                "user": post.user.username
            })
            
            
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "social",
            {
                'type': 'chat_message',
            }
        )       
        
        return Response({"user_posts": serialized_posts})




class AllPostsView(APIView):
    permission_classes = [userauthorization]
    def get(self, request):
        id=request.GET['token']['id']
        # fetchuser = Users.objects.filter(id = id).first()
        all_posts = UserPost.objects.filter().order_by('-time')
        
        serialized_posts = []  # List to store serialized post data
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "social",
            {
                'type': '',
            }
        )             
        
        for post in all_posts:
            serialized_posts.append({
                # "image": post.image.url if post.image else None,
                "caption": post.caption,
                "time": post.time,
                "user": post.user.username
            })
        
        return Response({"All Posts": serialized_posts})


