from models import User,Favorite
class UserService:
    def get_list(self):
        user_list=User.query.all()
        return [user.serialize() for user in user_list]
    
    def get_user(self, id):
        user = User.query.get(id)
        if user:
            return user.serialize()  
        return None  
    
    def get_favorite_list(self,user_id):
        favorite_list = Favorite.query.filter_by(user_id=user_id).all()
        return [favorite.serialize() for favorite in favorite_list]