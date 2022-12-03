import os
import requests
from django.conf import settings
from rest_framework.authtoken.models import Token
from account.models import UserModel
from e_shop.shortcuts import get_object_or_none,get_user_or_none
from rest_framework.views import APIView
from django.core import exceptions
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token as token_verifier
from google.auth.transport import requests as google_request
from account.serializers import UserSerializer


OAUTH_API_KEY =os.environ.get("OAUTH_API_KEY")

class GoogleLoginView(APIView):
    permission_classes =[]
    serializer_class = UserSerializer

    #convert cse.ariful@gmail.com => cse_ariful
    def get_username_from_email(self,email) -> str:
        return email.split("@")[0].replace('.','_') if '@' in email else None


    def save_profile_picture(self,image_url,username):
        file_name = f"{username}.png"
        save_path = os.path.join(settings.MEDIA_ROOT, "profile_pictures", file_name)
        picture_path = os.path.join("profile_pictures", file_name)
        response = requests.get(image_url)
        if response.status_code!=200:
            return None
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return picture_path

    
    def handle_id_token(self,id_token):
        try:
            info =  token_verifier.verify_oauth2_token(id_token,google_request.Request(),OAUTH_API_KEY)
            data = {
                'email':info['email'],
                'first_name':info['family_name'],
                'last_name':info['given_name'],
                'picture' : info['picture'],
                "is_email_verified": True,
            }
            return data
        except:
            raise exceptions.ValidationError("providerd id_token is invalid or issued for a different client")


    # obtain details from google api using access token
    def handle_access_token(self,access_token):
        ACCESS_TOKEN_INFO_ENDPOINT = "https://www.googleapis.com/userinfo/v2/me"
        oauth_response = requests.get(ACCESS_TOKEN_INFO_ENDPOINT,headers={"Authorization":f"Bearer {access_token}"})
    
        if not oauth_response.ok:
            raise exceptions.ValidationError(f"access token is not valid, status {oauth_response.status_code}")
        
        info = oauth_response.json()
        if not 'email' in info:
            # need to add email scope when signing in with google in client side
            raise exceptions.ValidationError("Please update the scope of google login with profile and email scope")
        data = { 
            'email':info['email'],
            'first_name':info['family_name'],
            'last_name':info['given_name'],
            'picture' : info['picture'],
            "is_email_verified": True,
        }
        return data



    '''
     request data format (one field is required)
     {
        'access_token": "access token from google sign in with profile and email scope",
        "id_token" : "id_token retrieved from google signin in client app"
     }
    '''
    def post(self,request):
        try:

            id_token = request.data.pop("id_token",None)
            access_token = request.data.pop("access_token",None)

            if not id_token and not access_token:
                raise exceptions.ValidationError("id_token or access_token is required")
            
            user_info = {}

            if id_token:
                info = self.handle_id_token(id_token=id_token)
                user_info.update(info)
            else:
                #exchange the user info from oauth using access_token
                info = self.handle_access_token(access_token)
                user_info.update(info)

            user = get_object_or_none(UserModel,email=user_info['email'])
            if user is not None:
                user.delete()
                user = None

            if user is None:
                #create new user
                username = self.get_username_from_email(user_info['email'])
                avatar = user_info.pop('picture',None)
                picture_path = self.save_profile_picture(avatar,username)
                user_info.update({
                    'username' : username
                })

                serializer = self.serializer_class(data=user_info)
               
                if serializer.is_valid():
                    serializer.validated_data['profile_picture'] = picture_path if picture_path else avatar
                    user = serializer.save() 
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)
            
            token = Token.objects.get_or_create(user=user)
            return Response(data ={"key":token[0].key}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":str(e)})
