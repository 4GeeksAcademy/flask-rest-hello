from models import People

class PeopleService:
    def get_list(self):
        people_list=People.query.all()
        return [person.serialize() for person in people_list]
    
    def get_people(self, id):
        person = People.query.get(id)
        if person:
            return person.serialize()  
        return None  

