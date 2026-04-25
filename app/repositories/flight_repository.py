from app.db.connection import get_connection


def get_flight_by_id(flight_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT * 
                FROM flight
                WHERE flight_id = %s
            """
            cursor.execute(query, (flight_id,))
            flight = cursor.fetchone()

        return flight

    finally:
        connection.close()