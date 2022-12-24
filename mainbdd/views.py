from django.shortcuts import render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import User, RealEstateAdd
from .serializers import UserSerializer, ReaSerializer, OfferSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView


class UserDetail(APIView):
    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


class ReasOfUser(APIView):
    def get_user(self,user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return user

    def get(self, request, user_id, format=None):
        user = self.get_user(user_id)
        reasOfUser = user.ownedReas.all()
        serializer = ReaSerializer(reasOfUser, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    def post(self, request, user_id, format=None):
        user = self.get_user(user_id=user_id)
        request.data['owner']=user_id
        serializer = ReaSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        if 'rea_to_delete_id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            rea = RealEstateAdd.objects.get(pk=request.data['rea_to_delete_id'])
        except RealEstateAdd.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if rea.owner.id != user_id:
            return Response({'rea not yours'},status=status.HTTP_400_BAD_REQUEST)
        
        rea.delete()
        return Response(status=status.HTTP_200_OK)
        

            
           



class FavsOfUser(APIView):
    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        favsOfUser = user.favorits.all()
        serializer = ReaSerializer(favsOfUser, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


class OffersOfRea(APIView):
    def get(self, request, rea_id, format=None):
        try:
            rea = RealEstateAdd.objects.get(pk=rea_id)
        except RealEstateAdd.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        offersOfRea = rea.offers.all()
        serializer = OfferSerializer(offersOfRea, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

































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
