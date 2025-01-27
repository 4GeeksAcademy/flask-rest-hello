from models import Planet

class PlanetService:
    def get_list(self):
        planet_list=Planet.query.all()
        return [planet.serialize() for planet in planet_list]
    
    def get_planet(self, id):
        planet = Planet.query.get(id)
        if planet:
            return planet.serialize()  
        return None  