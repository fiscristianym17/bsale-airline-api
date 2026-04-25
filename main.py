from fastapi import FastAPI
from app.repositories.flight_repository import get_flight_by_id
from app.repositories.passenger_repository import get_passengers_by_flight_id
from app.repositories.seat_repository import get_seats_by_airplane_id
from app.services.checkin_service import assign_seats
from app.services.checkin_service import validate_minors_with_adults

app = FastAPI(title="Bsale Airline API")

def format_passenger(passenger):
    return {
        "passengerId": passenger["passenger_id"],
        "dni": passenger["dni"],
        "name": passenger["name"],
        "age": passenger["age"],
        "country": passenger["country"],
        "boardingPassId": passenger["boarding_pass_id"],
        "purchaseId": passenger["purchase_id"],
        "seatTypeId": passenger["seat_type_id"],
        "seatId": passenger["seat_id"]
    }
    
@app.get("/")
def home():
    return {"message": "API funcionando correctamente"}


@app.get("/flights/{flight_id}")
def get_flight(flight_id: int):
    try:
        flight = get_flight_by_id(flight_id)

        if not flight:
            return {"code": 404, "data": {}}

        return {"code": 200, "data": flight}

    except Exception as error:
        return {"code": 400, "errors": str(error)}


@app.get("/flights/{flight_id}/passengers")
def get_flight_passengers(flight_id: int):
    try:
        flight = get_flight_by_id(flight_id)

        if not flight:
            return {"code": 404, "data": {}}

        passengers = get_passengers_by_flight_id(flight_id)
        seats = get_seats_by_airplane_id(flight["airplane_id"])
        passengers_with_seats = assign_seats(passengers, seats)
        #issues = validate_minors_with_adults(passengers_with_seats, seats)

        return {
            "code": 200,
            "data": {
                "flightId": flight["flight_id"],
                "takeoffDateTime": flight["takeoff_date_time"],
                "takeoffAirport": flight["takeoff_airport"],
                "landingDateTime": flight["landing_date_time"],
                "landingAirport": flight["landing_airport"],
                "airplaneId": flight["airplane_id"],
                "passengers": [format_passenger(p) for p in passengers_with_seats],
            }
        }

    except Exception as error:
        return {"code": 400, "errors": str(error)}