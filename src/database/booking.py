from .connection import db_connect
import datetime
def create_booking(room_id, user_id, date, start, end) -> int:
    with db_connect() as conn:
        with conn.cursor() as cur:
            start_time = datetime.datetime.strptime(f"{date} {start}", '%Y-%m-%d %H:%M')
            end_time = datetime.datetime.strptime(f"{date} {end}", '%Y-%m-%d %H:%M')
            if end_time <= start_time:
                raise ValueError("400 Bad Request: Конец бронирования должен быть позже начала")
            cur.execute(
                """
                SELECT id 
                FROM rooms
                WHERE id = %s
                FOR UPDATE;
                """,
                (room_id,)
            )
            room = cur.fetchone()
            if room is None:
                raise ValueError("404 Not Found: Выбранной комнаты не существует")
            cur.execute(
                """
                SELECT bookings.status, bookings.room_id, bookings.start_time, bookings.end_time
                FROM bookings
                WHERE bookings.room_id = %s 
                AND %s < bookings.end_time
                AND %s > bookings.start_time
                AND bookings.status = 'active';
                """,
                (room_id, start_time, end_time,)
            )
            conflict = cur.fetchone()
            if conflict is not None:
                raise ValueError("409 Conflict: Аудитория уже занята")
            cur.execute(
                """
                INSERT INTO bookings (room_id, start_time, end_time, status, user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (room_id, start_time, end_time, 'active', user_id)
            )
            booking_id = cur.fetchone()[0]
            return booking_id