from models import Starship

class StarshipService:
    def get_list(self):
        starship_list=Starship.query.all()
        return [starship.serialize() for starship in starship_list]
    
    def get_starship(self, id):
        starship = Starship.query.get(id)
        if starship:
            return starship.serialize()  
        return None  