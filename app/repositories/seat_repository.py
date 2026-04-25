from app.db.connection import get_connection


def get_seats_by_airplane_id(airplane_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    s.seat_id,
                    s.seat_column,
                    s.seat_row,
                    s.seat_type_id,
                    s.airplane_id
                FROM seat s
                WHERE s.airplane_id = %s
                ORDER BY s.seat_type_id, s.seat_row, s.seat_column
            """
            cursor.execute(query, (airplane_id,))
            return cursor.fetchall()

    finally:
        connection.close()