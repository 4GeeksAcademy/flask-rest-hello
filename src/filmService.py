from models import Film

class FilmService:
    def get_list(self):
        film_list=Film.query.all()
        return [film.serialize() for film in film_list]
    
    def get_film(self, id):
        film = Film.query.get(id)
        if film:
            return film.serialize()  
        return None  