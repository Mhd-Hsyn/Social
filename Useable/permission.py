from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework import status
# from decouple import config
import jwt




class userauthorization(permissions.BasePermission):

    def has_permission(self, request, view):
        try:

           
            tokencatch = request.META['HTTP_AUTHORIZATION'][7:]    #remove Bearer slicing from 8th char
            request.GET._mutable = True                            # making mutable, you can midify !!!! 
            my_token = jwt.decode(tokencatch,"abcd@123", algorithms=["HS256"])
            
            # my_token = jwt.decode(tokencatch,config('userjwttoken'), algorithms=["HS256"])
            
            
            request.GET['token'] = my_token
            
            # print(my_token)            
            
            # userwhitelistToken.objects.get(user = my_token['id'],token = tokencatch)
            return True
            

        except:
            raise NeedLogin()



class NeedLogin(APIException):
    status_code = 401
    default_detail = {'status': False, 'message': 'Unauthorized'}
    default_code = 'not_authenticated'