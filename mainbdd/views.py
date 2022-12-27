from django.shortcuts import render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import User, RealEstateAdd, Photo, Offer
from .serializers import UserSerializer, ReaSerializer, OfferSerializer, PhotoSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from .custom_renderers import PNGRenderer
from rest_framework.renderers import JSONRenderer
import jwt
import requests



class UserDetail(APIView):
    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_302_FOUND)



"""...........RealEsateAdd(s) -Rea(s) for short- Management..........."""



"""--->>> View for the post_rea endpoint"""
class PostRea(APIView):
    
    #Class Configuration
    parser_classes=[MultiPartParser,FormParser]
    
    """->Posts a rea for the user defined by the user_id url agrument"""
    """->Body contains: uploaded_photos, title, description, ... RealEstateAdd Model fields"""
    def post(self, request, user_id, format=None):
        files = request.FILES.getlist('uploaded_photos')
        if files:
            request.data.pop('uploaded_photos')
        request.data['owner']=user_id
        serializer = ReaSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            rea = serializer.save()
            for file in files:
                Photo(rea=rea, photo=file).save()
            serializer = ReaSerializer(rea)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""--->>> View for reas_of_user endpoint"""
class ReasOfUser(APIView):
    
    #Utilitary function
    def get_user(self,user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return user

    """->Gets all the reas of user defined by user_id url argument"""
    def get(self, request, user_id, format=None):
        user = self.get_user(user_id)
        reasOfUser = user.ownedReas.all()
        serializer = ReaSerializer(reasOfUser, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    """->Delete a rea from the owned reas of user defined by user_id url argument"""
    """->Body contains: rea_to_delete_id"""
    def delete(self, request, user_id, format=None):
        if 'rea_to_delete_id' not in request.data:
            return Response({'detail':'Missing rea_to_delete_id field'},status=status.HTTP_400_BAD_REQUEST)
        try:
            rea = RealEstateAdd.objects.get(pk=request.data['rea_to_delete_id'])
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea does not exit'},status=status.HTTP_404_NOT_FOUND)
        
        if rea.owner.id != user_id:
            return Response({'detail':'Rea is not owned by user'},status=status.HTTP_400_BAD_REQUEST)
        
        rea.delete()
        return Response(status=status.HTTP_200_OK)
      

"""--->>>View for the search_for_reas endpoint"""          
class SearchForReas(APIView):
    
    """->Gets all the reas corresponding to the search criteria"""
    """->Body contains: search_field, type, wilaya, commune, start_date, end_date"""
    """->start/end_date must be formated YYYY-MM-DD"""
    def get(self, request, format=None):

        token = request.headers.get('Authorization')
        id_token = token.rsplit("Bearer")[1]
        user = getUser(id_token)

        if not user :
            if 'search_field' not in request.data:
                return Response({'detail':'Missing search_field JSON field'},status=status.HTTP_400_BAD_REQUEST)
            
            if request.data['search_field'] == '':
                q= RealEstateAdd.objects.all()
            else:
                key_words = request.data['search_field'].split()
                q = RealEstateAdd.objects.none()
                for key_word in key_words:
                    q = q | RealEstateAdd.objects.filter(title__icontains=key_word) | RealEstateAdd.objects.filter(description__icontains=key_word)
                
            if request.data['type'] !='':
                q = q.filter(type=request.data['type'])
            if request.data['wilaya'] !='':
                q = q.filter(wilaya=request.data['wilaya'])
            if request.data['commune'] !='':
                q = q.filter(commune=request.data['commune'])
            if request.data['start_date'] != '':
                q = q.filter(pub_date__gte=request.data['start_date'])
            if request.data['end_date'] != '':
                q = q.filter(pub_date__lte=request.data['end_date'])
                    
            serializer = ReaSerializer(q, many=True)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        else : 
            Response(status="you don't have access")



"""...........Favorit(s) -Fav(s) for short- Management..........."""



"""--->>> View for favs_of_user endpoint"""   
    """->Gets all the favorits of the user defined by user_id url argument"""
    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        favsOfUser = user.favorits.all()
        serializer = ReaSerializer(favsOfUser, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    """->Registers a new favorit for the user defined by user_id url argument"""
    """->Body contains: rea_id"""
    def post(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail':'User was not found'},status=status.HTTP_400_BAD_REQUEST)
        
        if 'rea_id' not in request.data:
            return Response({'detail':'rea_id missing in request body'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rea = RealEstateAdd.objects.get(pk=request.data['rea_id'])
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'rea of rea_id was not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if rea.owner != user:
            user.favorits.add(rea)
            return Response(status=status.HTTP_200_OK)
        return Response({'detail':'Cannot add owned rea to favs'}, status=status.HTTP_400_BAD_REQUEST)
    
    """->Removes a rea from favorits of user defined by user_id url argument"""
    """->Body contains: rea_id"""
    def delete(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        if 'rea_id' not in request.data:
            return Response({'detail':'rea_id missing in body'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rea = RealEstateAdd.objects.get(pk=request.data['rea_id'])
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea of rea_id not found'}, status=status.HTTP_400_BAD_REQUEST)

        user.favorits.remove(rea)
        return Response(status=status.HTTP_200_OK)
        


"""...........Offers Managing..........."""



"""--->>> View for offers_made_by_user endpoint"""
class OffersMadeByUser(APIView):
    """->Gets all the offers made by the user defined by user_id"""
    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        offers = Offer.objects.filter(offerer=user)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


"""--->>> View for posting_offer endpoint"""
class PostingOffer(APIView):
    
    """->Posts a new offers for the rea definde by rea_id url terminal"""
    """->Body contains : description, proposal, offerer_id """
    def post(self, request, rea_id, format=None):
        try:
            rea = RealEstateAdd.objects.get(pk=rea_id)
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea of rea_id not found'},status=status.HTTP_404_NOT_FOUND)
        
        if  'description' not in request.data or 'proposal' not in request.data or 'offerer_id' not in request.data:
            return Response({'detail':'fields missing in request body'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['offerer_id']=='':
            return Response({'detail':'offerer_id must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(pk=request.data['offerer_id'])
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'User of offerer_id not found'}, status=status.HTTP_404_NOT_FOUND)
        offer = Offer(
                description=request.data['description'],
                proposal=request.data['proposal'],
                offerer=user,
                real_estate=rea).save()
        serializer = OfferSerializer(offer)        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""--->>> View for offers_of_rea endpoint"""
class OffersOfRea(APIView):
    
    """->Gets the offers related to the rea defined by rea_id"""
    def get(self, request, rea_id, format=None):
        try:
            rea = RealEstateAdd.objects.get(pk=rea_id)
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea of rea_id not found'},status=status.HTTP_404_NOT_FOUND)

        offersOfRea = rea.offers.all()
        serializer = OfferSerializer(offersOfRea, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
   

        






#LOGIN PART

def getUser(token):    
    user_json = jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IndhaWxrb3VpY2UwQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoic3doZmpkc2hqZmIgIiwiZmlyc3RfbmFtZSI6ImhvbWUiLCJsYXN0X25hbWUiOiJmIn0.KXZo-pkmPtBaj2UDmIaBCMxHzkISlrY53bmd4_hY2-s", "secret", algorithms=["HS256"])
    user = Account.objects.filter(email= user_json['email'],username= user_json['username']).first()
    return user


GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
def google_validate_id_token(id_token) -> bool:
   # response = requests.get(
    #    GOOGLE_ID_TOKEN_INFO_URL,
    #    params={'id_token':  id_token.rsplit("Bearer")[1]}
    #)
    return True 


@api_view(['POST'])
def login(request):
    id_token  = request.headers.get('Authorization')
    token_valide =  google_validate_id_token(id_token=id_token.replace("Bearer",""))
    user = UserSerializer(data =request.data)
    test = User.objects.filter(email= request.data['email']).first()
    if token_valide:
        if not test :
            if user.is_valid():
                user.save()
                return Response({
                'token': jwt.encode(request.data ,"secret", algorithm="HS256"),
                'status' : "200_signup",
                } )
            else : return Response(
             'email and username are not identical'
        )
        else :
            return Response({
            'token': jwt.encode(request.data, "secret", algorithm="HS256"),
            'status' : "200_login"
            } )
    else :
        return Response(
        status=status.HTTP_404_NOT_FOUND
        )         
























# def sepu():
#     print('---------------------------')
#     print(' ')
# def sepd():
#     print(' ')
#     print('---------------------------')

# class ProfileUpload(APIView):
#     parser_classes=[MultiPartParser,FormParser]
    
#     def post(self, request, format=None):
#         files = request.FILES.getlist('uploaded_files')
#         if files:
#             request.data.pop('uploaded_files')
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             pro = serializer.save()
#             pro_id = pro.id
#             for file in files:
#                 Photo(rea=pro, photo=file).save()
#             photos = pro.photos.all()
#             serializer = PhotoSerializer(photos, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class ProfileLoad(APIView):
#     #renderer_classes=[PNGRenderer]
#     def get(self, request,profile_id, format=None):
        
#         try:
#             profile = Profile.objects.get(pk=profile_id)
#         except Profile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class ProfileImagesLoad(APIView):
#     renderer_classes=[PNGRenderer]
#     def get(self, request,profile_id, format=None):
        
#         try:
#             profile = Profile.objects.get(pk=profile_id)
#         except Profile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         photos = []
#         for photo in profile.photos.all():
#             photos.append(photo.photo)
#         return Response({'loaded_photos':photos}, status=status.HTTP_200_OK)
    
            





# class ProfileUpload(APIView):
#     parser_classes=[MultiPartParser, FormParser]
#     renderer_classes=[PNGRenderer]
#     def post(self, request, format=None):
#         request.data['ufiles']
#         return Response(request.data['ufiles'], status=status.HTTP_200_OK)


#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#


# @api_view(['GET','POST'])
# def user_lc(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_302_FOUND)
    
#     elif request.method =='POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','DELETE','PUT'])
# def user_gdu(request,pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_302_FOUND)
#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(UserSerializer(User.objects.all(), many=True).data, status=status.HTTP_410_GONE)
#     elif request.method =='PUT':
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
