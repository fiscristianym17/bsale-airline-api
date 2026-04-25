from collections import defaultdict


def assign_seats(passengers, seats):
    occupied = {p["seat_id"] for p in passengers if p["seat_id"] is not None}

    available_seats = [
        s for s in seats
        if s["seat_id"] not in occupied
    ]

    available_seats.sort(
        key=lambda s: (s["seat_type_id"], s["seat_row"], s["seat_column"])
    )

    groups = defaultdict(list)

    for passenger in passengers:
        groups[passenger["purchase_id"]].append(passenger)

    result = []

    for purchase_id, group in groups.items():
        group.sort(key=lambda p: p["age"], reverse=True)

        adults = [p for p in group if p["age"] >= 18]
        minors = [p for p in group if p["age"] < 18]

        # Primero intentamos sentar menores al lado de adultos
        for minor in minors:
            if minor["seat_id"] is not None:
                continue

            adult = find_adult_without_seat_same_type(adults, minor)

            if adult:
                pair = find_adjacent_seats(
                    available_seats,
                    minor["seat_type_id"]
                )

                if pair:
                    adult["seat_id"] = pair[0]["seat_id"]
                    minor["seat_id"] = pair[1]["seat_id"]
                    available_seats.remove(pair[0])
                    available_seats.remove(pair[1])

        # Luego asignamos el resto del grupo
        for passenger in group:
            if passenger["seat_id"] is not None:
                result.append(passenger)
                continue

            seat = find_best_seat(
                available_seats,
                passenger["seat_type_id"]
            )

            if seat:
                passenger["seat_id"] = seat["seat_id"]
                available_seats.remove(seat)

            result.append(passenger)

    return result


def find_adult_without_seat_same_type(adults, minor):
    for adult in adults:
        if (
            adult["seat_id"] is None
            and adult["seat_type_id"] == minor["seat_type_id"]
        ):
            return adult

    return None


def find_adjacent_seats(available_seats, seat_type_id):
    seats_by_row = defaultdict(list)

    for seat in available_seats:
        if seat["seat_type_id"] == seat_type_id:
            seats_by_row[seat["seat_row"]].append(seat)

    for row, row_seats in seats_by_row.items():
        row_seats.sort(key=lambda s: s["seat_column"])

        for i in range(len(row_seats) - 1):
            current_seat = row_seats[i]
            next_seat = row_seats[i + 1]

            if are_adjacent_columns(
                current_seat["seat_column"],
                next_seat["seat_column"]
            ):
                return [current_seat, next_seat]

    return None


def are_adjacent_columns(column_a, column_b):
    return abs(ord(column_a) - ord(column_b)) == 1


def find_best_seat(available_seats, seat_type_id):
    for seat in available_seats:
        if seat["seat_type_id"] == seat_type_id:
            return seat

    return None

def validate_minors_with_adults(passengers, seats):
    seats_map = {s["seat_id"]: s for s in seats}

    issues = []

    groups = {}

    for p in passengers:
        groups.setdefault(p["purchase_id"], []).append(p)

    for purchase_id, group in groups.items():
        minors = [p for p in group if p["age"] < 18]
        adults = [p for p in group if p["age"] >= 18]

        for minor in minors:
            if minor["seat_id"] is None:
                issues.append({
                    "passengerId": minor["passenger_id"],
                    "problem": "Minor without seat"
                })
                continue

            minor_seat = seats_map.get(minor["seat_id"])

            if not minor_seat:
                continue

            row = minor_seat["seat_row"]
            col = minor_seat["seat_column"]

            found_adjacent_adult = False

            for adult in adults:
                if adult["seat_id"] is None:
                    continue

                adult_seat = seats_map.get(adult["seat_id"])

                if not adult_seat:
                    continue

                if adult_seat["seat_row"] == row:
                    if abs(ord(adult_seat["seat_column"]) - ord(col)) == 1:
                        found_adjacent_adult = True

            if not found_adjacent_adult:
                issues.append({
                    "passengerId": minor["passenger_id"],
                    "problem": "Minor not seated next to adult"
                })

    return issues