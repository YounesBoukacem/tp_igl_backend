from django.test import TestCase
from .models import User, RealEstateAdd, Offer
import json 
import jwt
import requests


class TestStringMethods(TestCase):

    def test_auth(self):
        headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhjMjdkYjRkMTNmNTRlNjU3ZDI2NWI0NTExMDA4MGI0ODhlYjQzOGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NzEyMDk5NTEsImF1ZCI6IjExMjQ1NjY5NjYyOS1jcWNwcmUzMXVxaWk3Z2RwZ2pnaWkzcmxyM2hzNG91aC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMTA2MzY4OTgwMzE0MjkyMDkxMSIsImVtYWlsIjoiYm91aGFtYXJtQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhenAiOiIxMTI0NTY2OTY2MjktY3FjcHJlMzF1cWlpN2dkcGdqZ2lpM3JscjNoczRvdWguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJuYW1lIjoiTWVkIEVtaXIgQm91aGFtYXIiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUVkRlRwNEZMb1E2YzVScGxTVnRZMHBib0RLTDFvb2ZmdmtPN0taM3YzQ3hDQT1zOTYtYyIsImdpdmVuX25hbWUiOiJNZWQgRW1pciIsImZhbWlseV9uYW1lIjoiQm91aGFtYXIiLCJpYXQiOjE2NzEyMTAyNTEsImV4cCI6MTY3MTIxMzg1MSwianRpIjoiYjMyNzhjZmE2NGJkMDJkMzM5OTdlMDUxODIxYjk2ODRjZDg0YmRlNiJ9.a8pOeXY2DugyWmWSGiRaaPRMldCzbBKzFBQcaC2KbYxQD8DqSyoA9ogF7YcWxFEKcRAxMftSdgYOeUguqHBKRntjaoaWGO7AIoMdstRow6dFexaPcewBs_7GeEq45e9YSAKbk3Pm_rigRgTDiQpUAiB3ongpsiGT7djZNKxBhh6SZy78HYHIaDxl_F_8lWaa8ZyGA0wf0y_ByYU7XSZc7QaXqYZ8fOPthj9kvDcFzBt4vp8NY6aAbTV2oilhKWu_I4ZvV_NzDK2boyATyXpncl_yzZA1drV9JP16-40Zvvqddl-HrjnI953W0BWe89p2koDcxkDNo3Zfc0PIAxwMLQ'}
        response = requests.post('http://127.0.0.1:8000/auth/', headers=headers , data={})


        jsonresp = json.loads(response.text)
        token = jsonresp['token']
        user_json = jwt.decode(token,"secret", algorithms=["HS256"])
        


        self.assertEqual(response.status_code,200) 
        self.assertEqual(user_json['email'],'bouhamarm@gmail.com')


    


    def test_CreateRea(self):

        user = User.objects.create(
            username = "user",
            first_name = "userfname",
            last_name = "userlname",
            picture = "",
            email = "user@gmail.com"
        )
        user.save()


        rea = RealEstateAdd.objects.create(
            title="rea1",
            description="description1",
            category = "category1",
            type = "type1",
            surface= 100,
            price = 100.0,
            localisation = "localisation1",
            longitude=10,
            latitude = 10,
            wilaya = "wilaya1",
            commune = "commune1",
            owner = user
        )

        rea.save()

        r = RealEstateAdd.objects.filter(title="rea1").first()

        self.assertEqual(str(r), 'rea1')




    def test_CreateOffre(self):
        user = User.objects.create(
            username = "user",
            first_name = "userfname",
            last_name = "userlname",
            picture = "",
            email = "wailkouicem0@gmail.com"
        )
        user.save()



        rea = RealEstateAdd.objects.create(
            title="rea1",
            description="description1",
            category = "category1",
            type = "type1",
            surface= 100,
            price = 100.0,
            localisation = "localisation1",
            longitude=10,
            latitude = 10,
            wilaya = "wilaya1",
            commune = "commune1",
            owner = user
        )
        rea.save()



        offer = Offer.objects.create(
            description = "descruption1",
            proposal = 100,
            offerer = user,
            real_estate = rea,
        )
        offer.save()
        o = Offer.objects.filter(description = "descruption1").first()

        self.assertEqual(str(o),"descruption1")