from app.db.connection import get_connection


def get_passengers_by_flight_id(flight_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    p.passenger_id,
                    p.dni,
                    p.name,
                    p.age,
                    p.country,
                    bp.boarding_pass_id,
                    bp.purchase_id,
                    bp.seat_type_id,
                    bp.seat_id
                FROM boarding_pass bp
                INNER JOIN passenger p 
                    ON p.passenger_id = bp.passenger_id
                WHERE bp.flight_id = %s
                ORDER BY bp.purchase_id, p.age DESC
            """
            cursor.execute(query, (flight_id,))
            return cursor.fetchall()

    finally:
        connection.close()