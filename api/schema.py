import json

from decouple import config as envs
from dal.firebase import fb
from graphene import Field, List, ObjectType, Schema
import urllib.request

from models.today_picture import TodayPicture
from exceptions import FetchException


class PicturesQuery(ObjectType):
    today_picture = Field(TodayPicture)
    last_picture = Field(TodayPicture)
    all_pictures = List(TodayPicture)

    def resolve_today_picture(self, info):
        try:
            with urllib.request.urlopen(f'https://api.nasa.gov/planetary/apod?api_key={envs("NASA_API_KEY")}') as response:
                response = json.loads(response.read().decode('utf-8'))
                return TodayPicture(title=response.get('title', ''),
                                    url=response.get('url', ''),
                                    description=response.get('explanation', ''),
                                    date=response.get('date', ''),
                                    author=response.get('author', ''))
        except:
            raise FetchException()
    
    def resolve_last_picture(self, info):
        last_picture = fb.get_last_picture()
        return TodayPicture(title=last_picture.get('title', ''),
                            url=last_picture.get('url', ''),
                            description=last_picture.get('explanation', ''),
                            date=last_picture.get('date', ''),
                            author=last_picture.get('author', ''))
    
    def resolve_all_pictures(self, info):
        all_pictures = fb.get_pictures()
        for picture in all_pictures:
            yield TodayPicture(title=picture.get('title', ''),
                               url=picture.get('url', ''),
                               description=picture.get('explanation', ''),
                               date=picture.get('date', ''),
                               author=picture.get('author', ''))


SCHEMA = Schema(query=PicturesQuery, types=[])
