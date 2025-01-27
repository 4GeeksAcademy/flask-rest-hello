from models import Vehicle

class VehicleService:
    def get_list(self):
        vehicle_list=Vehicle.query.all()
        return [vehicle.serialize() for vehicle in vehicle_list]
    
    def get_vehicle(self, id):
        vehicle = Vehicle.query.get(id)
        if vehicle:
            return vehicle.serialize()  
        return None  