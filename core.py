from datetime import datetime 
import vk_api
from pprint import pprint
from vk_api.exceptions import ApiError

from config import acces_token



class VkTools():
    def __init__(self, acces_token):
       self.api = vk_api.VkApi(token=acces_token)

    def get_profile_info(self, user_id):
        try:
            info, = self.api.method('users.get',
                                {'user_id': user_id,
                                'fields': 'city,bdate,sex,relation,home_town'
                                }
                                )
        except ApiError as e:
            info = {}
            print(f'error = {e}')

        user_info = {'name': info['first_name'] + ' '+ info['last_name'],
                     'id':  info['id'],
                     'bdate': info['bdate'] if 'bdate' in info else None,
                     'home_town': info['home_town'],
                     'sex': info['sex'],
                     'city': info['city']['id']
                     }

        if user_info ['bdate'] :
            curent_year = datetime.now().year
            user_year = int(user_info['bdate'].split('.')[2])
            user_info ['age'] = curent_year - user_year
        else:
            user_info['age'] = None

        return user_info
    
    def serch_users(self, params, offset):

        sex = 1 if params['sex'] == 2 else 2
        city = params['city']

        users = self.api.method('users.search',
                                {'count': 30,
                                 'offset': offset,
                                 'has_photo': True,
                                 'age_from': params['age'] - 5,
                                 'age_to': params['age'] + 5,
                                 'sex': sex,
                                 'city': city,
                                 'status': 6,
                                 'is_closed': False
                                }
                            )
        try:
            users = users['items']
        except KeyError:
            return []
        
        res = []

        for user in users:
            if user['is_closed'] == False:
                res.append({'id' : user['id'],
                            'name': user['first_name'] + ' ' + user['last_name']
                           }
                           )
        
        return res

    def get_photos(self, user_id):
        photos = self.api.method('photos.get',
                                 {'user_id': user_id,
                                  'album_id': 'profile',
                                  'extended': 1
                                 }
                                )
        try:
            photos = photos['items']
        except KeyError:
            return []
        
        res = []

        for photo in photos:
            res.append({'owner_id': photo['owner_id'],
                        'id': photo['id'],
                        'likes': photo['likes']['count'],
                        'comments': photo['comments']['count'],
                        }
                        )
            
        res.sort(key=lambda x: x['likes']+x['comments']*10, reverse=True)

        return res


if __name__ == '__main__':
    bot = VkTools(acces_token)
    params = bot.get_profile_info(1653668)
    users = bot.serch_users(params)
    pprint(bot.get_photos(users[2]['id']))
    # pprint(users)

