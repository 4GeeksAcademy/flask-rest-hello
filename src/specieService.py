from models import Specie

class SpecieService:
    def get_list(self):
        specie_list=Specie.query.all()
        return [specie.serialize() for specie in specie_list]
    
    def get_specie(self, id):
        specie = Specie.query.get(id)
        if specie:
            return specie.serialize()  
        return None  