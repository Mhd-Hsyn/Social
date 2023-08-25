import jwt
import datetime



def usergeneratedToken(fetchuser,authKey,totaldays,request):
    try:
        access_token_payload = {
            'id': str(fetchuser.id),
            'email':fetchuser.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=totaldays),
            'iat': datetime.datetime.utcnow(),

        }
        
        userpayload = { 'id': str(fetchuser.id),'email':fetchuser.email,'fname':fetchuser.fname,'lname':fetchuser.lname, 'profile': fetchuser.profile.url}
        
        # ,'profile':fetchuser.profile.url
    
        access_token = jwt.encode(access_token_payload,authKey, algorithm='HS256')
        # userwhitelistToken(user = fetchuser,token = access_token).save()
        return {"status":True,"token":access_token,"payload":userpayload}

    except Exception as e:
        return {"status":False,"message":"Something went wrong in token creation","details":str(e)}

