from flask import Flask, render_template, request, redirect, session
import mysql.connector
import random
import os

app = Flask(__name__)
app.secret_key = "railbook_demo_secret_key"


# =========================================================
# DATABASE
# =========================================================


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        port=int(os.environ.get("MYSQLPORT", 3306)),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE")
    )


# =========================================================
# ADMIN CHECK
# =========================================================

def admin_required():
    return "admin_id" in session


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize(value):

    if value is None:
        return ""

    return str(value).strip().lower()


class_aliases = {

    "ac chair car": "AC Chair Car",

    "ac 3 tier": "AC 3 Tier",

    "ac 2 tier": "AC 2 Tier",

    "first ac": "First AC",

    "sleeper": "Sleeper",

    "second sitting": "Second Sitting"
}


def get_fare(train_class):

    fares = {

        "AC Chair Car": 650,

        "AC 3 Tier": 950,

        "AC 2 Tier": 1400,

        "First AC": 1900,

        "Sleeper": 350,

        "Second Sitting": 180

    }

    return fares.get(
        train_class,
        350
    )


# =========================================================
# TRAIN DATA
# =========================================================

trains = [

    {
        "number": "12124",
        "name": "Deccan Queen",
        "from": "Pune",
        "to": "Mumbai",
        "departure": "07:15",
        "arrival": "10:25",
        "duration": "3h 10m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "12125",
        "name": "Pragati Express",
        "from": "Pune",
        "to": "Mumbai",
        "departure": "06:30",
        "arrival": "09:55",
        "duration": "3h 25m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "11010",
        "name": "Sinhagad Express",
        "from": "Pune",
        "to": "Mumbai",
        "departure": "09:20",
        "arrival": "12:50",
        "duration": "3h 30m",
        "class": "Second Sitting",
        "classes": [
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "11030",
        "name": "Koyna Express",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "08:40",
        "arrival": "12:05",
        "duration": "3h 25m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "12127",
        "name": "Intercity Express",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "06:40",
        "arrival": "10:05",
        "duration": "3h 25m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "11007",
        "name": "Deccan Express",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "15:20",
        "arrival": "18:50",
        "duration": "3h 30m",
        "class": "Second Sitting",
        "classes": [
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "12129",
        "name": "Mumbai Pune Intercity",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "17:50",
        "arrival": "21:05",
        "duration": "3h 15m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "11009",
        "name": "Sinhagad Express",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "09:10",
        "arrival": "12:40",
        "duration": "3h 30m",
        "class": "Second Sitting",
        "classes": [
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "12123",
        "name": "Deccan Queen",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "17:10",
        "arrival": "20:25",
        "duration": "3h 15m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "11020",
        "name": "Konark Express",
        "from": "Pune",
        "to": "Mumbai",
        "departure": "11:30",
        "arrival": "15:20",
        "duration": "3h 50m",
        "class": "Sleeper",
        "classes": [
                    "Sleeper",
                    "AC 3 Tier",
                    "AC 2 Tier",
                    "First AC"
                ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "22150",
        "name": "Pune Mumbai Superfast",
        "from": "Pune",
        "to": "Mumbai",
        "departure": "13:15",
        "arrival": "16:30",
        "duration": "3h 15m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "22149",
        "name": "Mumbai Pune Superfast",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "14:00",
        "arrival": "17:20",
        "duration": "3h 20m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "11028",
        "name": "Chennai Mail",
        "from": "Pune",
        "to": "Mumbai",
        "departure": "18:20",
        "arrival": "22:00",
        "duration": "3h 40m",
        "class": "Sleeper",
        "classes": [
            "Sleeper"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "12110",
        "name": "Panchavati Express",
        "from": "Mumbai",
        "to": "Pune",
        "departure": "06:10",
        "arrival": "09:30",
        "duration": "3h 20m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    },

    {
        "number": "12111",
        "name": "Panchavati Express",
        "from": "Pune",
        "to": "Mumbai",
        "departure": "18:00",
        "arrival": "21:30",
        "duration": "3h 30m",
        "class": "AC Chair Car",
        "classes": [
            "AC Chair Car",
            "Second Sitting"
        ],
        "seats": 24,
        "status": "Running"
    }
]


# =========================================================
# TRAIN RUNNING STATUS
# SIMULATED DATA FOR PROJECT
# =========================================================

train_status = {

    "12124": {
        "status": "Running",
        "current": "Lonavala",
        "next": "Khandala",
        "delay": "On Time",
        "platform": "Platform 2"
    },

    "12125": {
        "status": "Running",
        "current": "Khadki",
        "next": "Shivajinagar",
        "delay": "5 Minutes Late",
        "platform": "Platform 4"
    },

    "11010": {
        "status": "Running",
        "current": "Shivajinagar",
        "next": "Khadki",
        "delay": "On Time",
        "platform": "Platform 1"
    },

    "11030": {
        "status": "Running",
        "current": "Dadar",
        "next": "Thane",
        "delay": "10 Minutes Late",
        "platform": "Platform 5"
    },

    "12127": {
        "status": "Running",
        "current": "Thane",
        "next": "Kalyan",
        "delay": "On Time",
        "platform": "Platform 6"
    },

    "11007": {
        "status": "Running",
        "current": "Dadar",
        "next": "Kurla",
        "delay": "3 Minutes Late",
        "platform": "Platform 3"
    },

    "12129": {
        "status": "Running",
        "current": "Kalyan",
        "next": "Dadar",
        "delay": "On Time",
        "platform": "Platform 7"
    },

    "11009": {
        "status": "Running",
        "current": "Thane",
        "next": "Kalyan",
        "delay": "7 Minutes Late",
        "platform": "Platform 5"
    },

    "12123": {
        "status": "Running",
        "current": "Kalyan",
        "next": "Karjat",
        "delay": "On Time",
        "platform": "Platform 2"
    },

    "11020": {
        "status": "Running",
        "current": "Lonavala",
        "next": "Khandala",
        "delay": "12 Minutes Late",
        "platform": "Platform 1"
    },

    "22150": {
        "status": "Running",
        "current": "Khadki",
        "next": "Lonavala",
        "delay": "On Time",
        "platform": "Platform 4"
    },

    "22149": {
        "status": "Running",
        "current": "Thane",
        "next": "Dadar",
        "delay": "6 Minutes Late",
        "platform": "Platform 3"
    },

    "11028": {
        "status": "Running",
        "current": "Pune",
        "next": "Lonavala",
        "delay": "15 Minutes Late",
        "platform": "Platform 6"
    },

    "12110": {
        "status": "Running",
        "current": "Dadar",
        "next": "Thane",
        "delay": "On Time",
        "platform": "Platform 2"
    },

    "12111": {
        "status": "Running",
        "current": "Khadki",
        "next": "Lonavala",
        "delay": "4 Minutes Late",
        "platform": "Platform 1"
    }
}


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "index.html",
        trains=trains
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        db = get_db_connection()
        cursor = db.cursor()
        print("REGISTER ROUTE - NEW CODE")

        try:

            cursor.execute("""
                INSERT INTO users
                (name, email, mobile, password)
                VALUES (%s, %s, %s, %s)
            """, (
                name,
                email,
                mobile,
                password
            ))

            db.commit()

        except mysql.connector.Error as e:

            cursor.close()
            db.close()

            return "TEST ERROR: " + str(e)

        cursor.close()
        db.close()

        return redirect("/login")

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email = %s
            AND password = %s
        """, (
            email,
            password
        ))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["user_email"] = user["email"]

            return redirect("/")

        return "Invalid email or password."

    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.pop(
        "user_id",
        None
    )

    session.pop(
        "user_name",
        None
    )

    session.pop(
        "user_email",
        None
    )

    return redirect("/")


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db_connection()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM users
        WHERE id = %s
    """, (
        session["user_id"],
    ))

    user = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "profile.html",
        user=user
    )


# =========================================================
# TRAIN SEARCH
# =========================================================

@app.route(
    "/search",
    methods=["POST"]
)
def search():

    if "user_id" not in session:
        return redirect("/login")

    from_station = request.form.get(
        "from_station",
        ""
    ).strip()

    to_station = request.form.get(
        "to_station",
        ""
    ).strip()

    journey_date = request.form.get(
        "journey_date",
        ""
    ).strip()

    train_class_input = request.form.get(
        "train_class",
        ""
    ).strip()

    train_class = class_aliases.get(
        normalize(train_class_input),
        train_class_input
    )
    print("SELECTED CLASS:", repr(train_class_input))
    print("FINAL CLASS:", repr(train_class))

    results = []

    db = get_db_connection()
    cursor = db.cursor()

    for train in trains:

        route_match = (
            normalize(train["from"])
            ==
            normalize(from_station)
            and
            normalize(train["to"])
            ==
            normalize(to_station)
        )

        available_classes = train.get(
            "classes",
            [train.get("class", "")]
        )

        class_match = any(
            normalize(train_class)
            ==
            normalize(available_class)
            for available_class in available_classes
        )

        if route_match and class_match:

            cursor.execute("""
                SELECT COUNT(*)
                FROM bookings
                WHERE train_number = %s
                AND journey_date = %s
                AND train_class = %s
            """, (
                train["number"],
                journey_date,
                train_class
            ))

            booked_count = cursor.fetchone()[0]

            train_copy = train.copy()

            train_copy["class"] = train_class

            train_copy["seats"] = max(
                0,
                24 - booked_count
            )

            train_copy["fare"] = get_fare(
                train_class
            )

            train_copy["duration"] = train.get(
                "duration",
                "Not Available"
            )

            train_copy["classes"] = available_classes

            results.append(train_copy)

    cursor.close()
    db.close()

    return render_template(
        "search_results.html",
        trains=results,
        from_station=from_station,
        to_station=to_station,
        journey_date=journey_date,
        train_class=train_class
    )


# =========================================================
# PASSENGER DETAILS
# =========================================================

@app.route(
    "/passenger-details",
    methods=["POST"]
)
def passenger_details():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "passenger_details.html",

        train_number=request.form.get(
            "train_number",
            ""
        ),

        train_name=request.form.get(
            "train_name",
            ""
        ),

        from_station=request.form.get(
            "from_station",
            ""
        ),

        to_station=request.form.get(
            "to_station",
            ""
        ),

        journey_date=request.form.get(
            "journey_date",
            ""
        ),

        train_class=request.form.get(
            "train_class",
            ""
        ),

        fare=request.form.get(
            "fare",
            "0"
        )
    )


# =========================================================
# SEAT SELECTION
# =========================================================

@app.route(
    "/seat-selection",
    methods=["POST"]
)
def seat_selection():

    if "user_id" not in session:
        return redirect("/login")

    train_number = request.form.get(
        "train_number",
        ""
    )

    train_name = request.form.get(
        "train_name",
        ""
    )

    from_station = request.form.get(
        "from_station",
        ""
    )

    to_station = request.form.get(
        "to_station",
        ""
    )

    journey_date = request.form.get(
        "journey_date",
        ""
    )

    train_class_input = request.form.get(
        "train_class",
        ""
    )

    train_class = class_aliases.get(
        normalize(train_class_input),
        train_class_input
    )

    fare = request.form.get(
        "fare",
        "0"
    )

    passenger_names = request.form.getlist(
        "passenger_name[]"
    )

    ages = request.form.getlist(
        "age[]"
    )

    genders = request.form.getlist(
        "gender[]"
    )

    mobiles = request.form.getlist(
        "mobile[]"
    )

    seat_preferences = request.form.getlist(
        "seat_preference[]"
    )

    # Old single passenger form support

    if not passenger_names:

        old_name = request.form.get(
            "passenger_name",
            ""
        )

        if old_name:

            passenger_names = [
                old_name
            ]

            ages = [
                request.form.get(
                    "age",
                    ""
                )
            ]

            genders = [
                request.form.get(
                    "gender",
                    ""
                )
            ]

            mobiles = [
                request.form.get(
                    "mobile",
                    ""
                )
            ]

            seat_preferences = [
                request.form.get(
                    "seat_preference",
                    ""
                )
            ]

    passenger_count = len(
        passenger_names
    )

    if passenger_count < 1:

        return """
        <script>
            alert("Please add at least one passenger.");
            window.history.back();
        </script>
        """

    if passenger_count > 6:

        return """
        <script>
            alert("Maximum 6 passengers are allowed.");
            window.history.back();
        </script>
        """

    if not (
        len(ages) == passenger_count
        and
        len(genders) == passenger_count
        and
        len(mobiles) == passenger_count
    ):

        return """
        <script>
            alert("Please enter complete details for all passengers.");
            window.history.back();
        </script>
        """

    while len(
        seat_preferences
    ) < passenger_count:

        seat_preferences.append("")

    db = get_db_connection()

    cursor = db.cursor()

    cursor.execute("""
        SELECT seat_number
        FROM bookings
        WHERE train_number = %s
        AND journey_date = %s
        AND train_class = %s
    """, (
        train_number,
        journey_date,
        train_class
    ))

    booked_seats = [

        row[0]

        for row in cursor.fetchall()

        if row[0]
    ]

    cursor.close()
    db.close()

    seats = []

    for i in range(1, 25):

        seat_number = f"S1-{i:02d}"

        seats.append({

            "number":
                seat_number,

            "booked":
                seat_number in booked_seats

        })

    return render_template(

        "seat_selection.html",

        seats=seats,

        booked_seats=booked_seats,

        passenger_names=passenger_names,

        ages=ages,

        genders=genders,

        mobiles=mobiles,

        seat_preferences=seat_preferences,

        passenger_count=passenger_count,

        train_number=train_number,

        train_name=train_name,

        from_station=from_station,

        to_station=to_station,

        journey_date=journey_date,

        train_class=train_class,

        fare=fare
    )


# =========================================================
# BOOK TRAIN
# =========================================================

@app.route(
    "/book",
    methods=["POST"]
)
@app.route(
    "/book-train",
    methods=["POST"]
)
def book():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    train_number = request.form.get(
        "train_number",
        ""
    )

    train_name = request.form.get(
        "train_name",
        ""
    )

    from_station = request.form.get(
        "from_station",
        ""
    )

    to_station = request.form.get(
        "to_station",
        ""
    )

    journey_date = request.form.get(
        "journey_date",
        ""
    )

    train_class_input = request.form.get(
        "train_class",
        ""
    )

    train_class = class_aliases.get(
        normalize(train_class_input),
        train_class_input
    )

    try:

        fare_per_passenger = float(
            request.form.get(
                "fare",
                "0"
            )
        )

    except ValueError:

        fare_per_passenger = get_fare(
            train_class
        )

    if fare_per_passenger <= 0:

        fare_per_passenger = get_fare(
            train_class
        )

    # -----------------------------------------------------
    # PASSENGER DETAILS
    # -----------------------------------------------------

    passenger_names = request.form.getlist(
        "passenger_name[]"
    )

    ages = request.form.getlist(
        "age[]"
    )

    genders = request.form.getlist(
        "gender[]"
    )

    mobiles = request.form.getlist(
        "mobile[]"
    )

    if not passenger_names:

        passenger_name = request.form.get(
            "passenger_name",
            ""
        )

        if passenger_name:

            passenger_names = [
                passenger_name
            ]

            ages = [
                request.form.get(
                    "age",
                    ""
                )
            ]

            genders = [
                request.form.get(
                    "gender",
                    ""
                )
            ]

            mobiles = [
                request.form.get(
                    "mobile",
                    ""
                )
            ]

    passenger_count = len(
        passenger_names
    )

    if passenger_count < 1:

        return """
        <script>
            alert("Please add at least one passenger.");
            window.history.back();
        </script>
        """

    if passenger_count > 6:

        return """
        <script>
            alert("Maximum 6 passengers are allowed.");
            window.history.back();
        </script>
        """

    if not (
        len(ages) == passenger_count
        and
        len(genders) == passenger_count
        and
        len(mobiles) == passenger_count
    ):

        return """
        <script>
            alert("Please enter complete passenger details.");
            window.history.back();
        </script>
        """

    # -----------------------------------------------------
    # SEATS
    # -----------------------------------------------------

    seat_numbers = request.form.getlist(
        "seat_number[]"
    )

    if not seat_numbers:

        old_seat = request.form.get(
            "seat_number",
            ""
        )

        if old_seat:

            seat_numbers = [
                old_seat
            ]

    if len(seat_numbers) != passenger_count:

        return """
        <script>
            alert("Please select one seat for every passenger.");
            window.history.back();
        </script>
        """

    seat_numbers = [

        seat.strip()

        for seat in seat_numbers
    ]

    if len(
        set(seat_numbers)
    ) != len(seat_numbers):

        return """
        <script>
            alert("Two passengers cannot have the same seat.");
            window.history.back();
        </script>
        """

    valid_seats = {

        f"S1-{i:02d}"

        for i in range(1, 25)
    }

    if any(

        seat not in valid_seats

        for seat in seat_numbers
    ):

        return """
        <script>
            alert("Invalid seat selected.");
            window.history.back();
        </script>
        """

    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    db = get_db_connection()

    cursor = db.cursor()

    try:

        cursor.execute("""
            SELECT seat_number
            FROM bookings
            WHERE train_number = %s
            AND journey_date = %s
            AND train_class = %s
        """, (
            train_number,
            journey_date,
            train_class
        ))

        booked_seats = {

            row[0]

            for row in cursor.fetchall()

            if row[0]
        }

        already_booked = [

            seat

            for seat in seat_numbers

            if seat in booked_seats
        ]

        if already_booked:

            db.rollback()

            cursor.close()
            db.close()

            return """
            <script>
                alert("One or more selected seats are already booked. Please select different seats.");
                window.history.back();
            </script>
            """

        if (
            len(booked_seats)
            +
            passenger_count
            >
            24
        ):

            db.rollback()

            cursor.close()
            db.close()

            return """
            <script>
                alert("Not enough seats are available for all passengers.");
                window.history.back();
            </script>
            """

        # -------------------------------------------------
        # PNR
        # -------------------------------------------------

        pnr = None

        for _ in range(20):

            candidate = str(
                random.randint(
                    1000000000,
                    9999999999
                )
            )

            cursor.execute("""
                SELECT id
                FROM bookings
                WHERE pnr = %s
                LIMIT 1
            """, (
                candidate,
            ))

            if not cursor.fetchone():

                pnr = candidate

                break

        if not pnr:

            raise Exception(
                "Unable to generate unique PNR."
            )

        # -------------------------------------------------
        # BOOKING ID
        # -------------------------------------------------

        booking_id = None

        for _ in range(20):

            candidate_booking_id = (

                "RB"

                +

                str(
                    random.randint(
                        100000000000,
                        999999999999
                    )
                )
            )

            cursor.execute("""
                SELECT id
                FROM bookings
                WHERE booking_id = %s
                LIMIT 1
            """, (
                candidate_booking_id,
            ))

            if not cursor.fetchone():

                booking_id = candidate_booking_id

                break

        if not booking_id:

            raise Exception(
                "Unable to generate booking ID."
            )

        # -------------------------------------------------
        # INSERT PASSENGERS
        # -------------------------------------------------

        for i in range(
            passenger_count
        ):

            cursor.execute("""
                INSERT INTO bookings
                (
                    booking_id,
                    user_id,
                    pnr,
                    passenger_name,
                    age,
                    gender,
                    mobile,
                    train_number,
                    train_name,
                    from_station,
                    to_station,
                    journey_date,
                    train_class,
                    fare,
                    seat_number
                )
                VALUES
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """, (
                booking_id,

                user_id,

                pnr,

                passenger_names[i],

                ages[i],

                genders[i],

                mobiles[i],

                train_number,

                train_name,

                from_station,

                to_station,

                journey_date,

                train_class,

                fare_per_passenger,

                seat_numbers[i]
            ))

        db.commit()

    except Exception:

        db.rollback()

        cursor.close()
        db.close()

        return """
        <script>
            alert("Booking failed. Please try again.");
            window.history.back();
        </script>
        """

    cursor.close()
    db.close()

    total_fare = (

        fare_per_passenger

        *

        passenger_count
    )

    return render_template(

        "booking_confirmation.html",

        pnr=pnr,

        booking_id=booking_id,

        passenger_name=passenger_names[0],

        age=ages[0],

        gender=genders[0],

        mobile=mobiles[0],

        train_number=train_number,

        train_name=train_name,

        from_station=from_station,

        to_station=to_station,

        journey_date=journey_date,

        train_class=train_class,

        seat_number=seat_numbers[0],

        fare=fare_per_passenger,

        total_fare=total_fare,

        passenger_count=passenger_count,

        passengers=[

            {

                "name":
                    passenger_names[i],

                "age":
                    ages[i],

                "gender":
                    genders[i],

                "mobile":
                    mobiles[i],

                "seat_number":
                    seat_numbers[i]

            }

            for i in range(
                passenger_count
            )
        ]
    )


# =========================================================
# MY BOOKINGS
# =========================================================

@app.route("/my-bookings")
def my_bookings():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db_connection()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM bookings
        WHERE user_id = %s
        ORDER BY id DESC
    """, (
        session["user_id"],
    ))

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    grouped = {}

    for row in rows:

        group_key = (

            row.get("booking_id")

            or

            f"OLD-{row['id']}"
        )

        if group_key not in grouped:

            grouped[group_key] = {

                "booking_id":
                    row.get("booking_id"),

                "pnr":
                    row.get("pnr"),

                "train_number":
                    row.get("train_number"),

                "train_name":
                    row.get("train_name"),

                "from_station":
                    row.get("from_station"),

                "to_station":
                    row.get("to_station"),

                "journey_date":
                    row.get("journey_date"),

                "train_class":
                    row.get("train_class"),

                "fare":
                    0,

                "passenger_count":
                    0,

                "passengers":
                    [],

                "id":
                    row["id"]
            }

        grouped[group_key]["fare"] += float(
            row.get("fare") or 0
        )

        grouped[group_key][
            "passenger_count"
        ] += 1

        grouped[group_key][
            "passengers"
        ].append(row)

    bookings = list(
        grouped.values()
    )

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )


# =========================================================
# PNR STATUS
# =========================================================

@app.route(
    "/pnr-status",
    methods=["GET", "POST"]
)
def pnr_status():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        pnr = request.form.get(
            "pnr",
            ""
        ).strip()

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT *
            FROM bookings
            WHERE pnr = %s
            AND user_id = %s
            ORDER BY id ASC
        """, (
            pnr,
            session["user_id"]
        ))

        passengers = cursor.fetchall()

        cursor.close()
        db.close()

        if not passengers:

            return render_template(

                "pnr_result.html",

                booking=None,

                passengers=[],

                passenger_count=0,

                total_fare=0
            )

        total_fare = sum(

            float(
                row.get("fare") or 0
            )

            for row in passengers
        )

        return render_template(

            "pnr_result.html",

            booking=passengers[0],

            passengers=passengers,

            passenger_count=len(
                passengers
            ),

            total_fare=total_fare
        )

    return render_template(
        "pnr_status.html"
    )


# =========================================================
# CANCEL BOOKING
# =========================================================

@app.route(
    "/cancel-booking",
    methods=["POST"]
)
def cancel_booking():

    if "user_id" not in session:
        return redirect("/login")

    booking_id = request.form.get(
        "booking_id",
        ""
    ).strip()

    pnr = request.form.get(
        "pnr",
        ""
    ).strip()

    db = get_db_connection()

    cursor = db.cursor()

    if booking_id:

        cursor.execute("""
            DELETE FROM bookings
            WHERE booking_id = %s
            AND user_id = %s
        """, (
            booking_id,
            session["user_id"]
        ))

    elif pnr:

        cursor.execute("""
            DELETE FROM bookings
            WHERE pnr = %s
            AND user_id = %s
        """, (
            pnr,
            session["user_id"]
        ))

    else:

        old_id = request.form.get(
            "id"
        )

        cursor.execute("""
            DELETE FROM bookings
            WHERE id = %s
            AND user_id = %s
        """, (
            old_id,
            session["user_id"]
        ))

    db.commit()

    cursor.close()
    db.close()

    return redirect(
        "/my-bookings"
    )


# =========================================================
# TRAIN RUNNING STATUS
# =========================================================

@app.route(
    "/train-status",
    methods=["GET", "POST"]
)
def train_running_status():

    result = None

    train_number = ""

    if request.method == "POST":

        train_number = request.form.get(
            "train_number",
            ""
        ).strip()

        selected_train = None

        for train in trains:

            if str(
                train.get("number", "")
            ) == train_number:

                selected_train = train

                break

        if train_number in train_status:

            status_data = train_status[
                train_number
            ]

            result = {

                "train_number":
                    train_number,

                "train_name":
                    (
                        selected_train["name"]

                        if selected_train

                        else "RailBook Express"
                    ),

                "status":
                    status_data.get(
                        "status",
                        "Running"
                    ),

                "current_station":
                    status_data.get(
                        "current",
                        "Not Available"
                    ),

                "next_station":
                    status_data.get(
                        "next",
                        "Not Available"
                    ),

                "delay":
                    status_data.get(
                        "delay",
                        "On Time"
                    ),

                "platform":
                    status_data.get(
                        "platform",
                        "Not Available"
                    )
            }

    return render_template(

        "train_status.html",

        trains=trains,

        train_status=train_status,

        result=result,

        train_number=train_number
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin-login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT *
            FROM admins
            WHERE email = %s
            AND password = %s
        """, (
            email,
            password
        ))

        admin = cursor.fetchone()

        cursor.close()
        db.close()

        if admin:

            session["admin_id"] = admin[
                "id"
            ]

            session["admin_name"] = admin[
                "name"
            ]

            return redirect(
                "/admin-dashboard"
            )

        return (
            "Invalid admin email "
            "or password."
        )

    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin-logout")
def admin_logout():

    session.pop(
        "admin_id",
        None
    )

    session.pop(
        "admin_name",
        None
    )

    return redirect(
        "/admin-login"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route(
    "/admin-dashboard",
    methods=["GET", "POST"]
)
def admin_dashboard():

    if not admin_required():

        return redirect(
            "/admin-login"
        )

    search = ""

    db = get_db_connection()

    cursor = db.cursor(
        dictionary=True
    )

    if request.method == "POST":

        search = request.form.get(
            "search",
            ""
        ).strip()

    if search:

        like = "%" + search + "%"

        cursor.execute("""
            SELECT *
            FROM bookings
            WHERE pnr LIKE %s
            OR booking_id LIKE %s
            OR passenger_name LIKE %s
            OR train_number LIKE %s
            ORDER BY id DESC
        """, (
            like,
            like,
            like,
            like
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM bookings
            ORDER BY id DESC
        """)

    bookings = cursor.fetchall()

    # Total bookings

    cursor.execute("""
        SELECT COUNT(DISTINCT
            CASE
                WHEN booking_id IS NULL
                OR booking_id = ''
                THEN CONCAT('OLD-', id)
                ELSE booking_id
            END
        ) AS total_bookings
        FROM bookings
    """)

    total_bookings = cursor.fetchone()[
        "total_bookings"
    ]

    # Total passengers

    cursor.execute("""
        SELECT COUNT(*) AS total_passengers
        FROM bookings
    """)

    total_passengers = cursor.fetchone()[
        "total_passengers"
    ]

    # Revenue

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(fare),
                0
            ) AS total_revenue
        FROM bookings
    """)

    total_revenue = float(
        cursor.fetchone()[
            "total_revenue"
        ] or 0
    )

    cursor.close()
    db.close()

    available_trains = len(
        trains
    )

    return render_template(

        "admin_dashboard.html",

        bookings=bookings,

        admin_name=session.get(
            "admin_name",
            "Admin"
        ),

        search=search,

        total_bookings=
            total_bookings,

        total_passengers=
            total_passengers,

        total_revenue=
            total_revenue,

        available_trains=
            available_trains
    )


# =========================================================
# ADMIN BOOKING DETAILS
# =========================================================

@app.route(
    "/admin-booking/<int:booking_id>"
)
def admin_booking_details(
    booking_id
):

    if not admin_required():

        return redirect(
            "/admin-login"
        )

    db = get_db_connection()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM bookings
        WHERE id = %s
    """, (
        booking_id,
    ))

    first_booking = cursor.fetchone()

    if not first_booking:

        cursor.close()
        db.close()

        return redirect(
            "/admin-dashboard"
        )

    group_booking_id = (
        first_booking.get(
            "booking_id"
        )
    )

    pnr = first_booking.get(
        "pnr"
    )

    if group_booking_id:

        cursor.execute("""
            SELECT *
            FROM bookings
            WHERE booking_id = %s
            ORDER BY id ASC
        """, (
            group_booking_id,
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM bookings
            WHERE pnr = %s
            ORDER BY id ASC
        """, (
            pnr,
        ))

    passengers = cursor.fetchall()

    cursor.close()
    db.close()

    total_fare = sum(

        float(
            row.get("fare") or 0
        )

        for row in passengers
    )

    return render_template(

        "admin_booking_details.html",

        booking=first_booking,

        passengers=passengers,

        passenger_count=len(
            passengers
        ),

        total_fare=total_fare,

        admin_name=session.get(
            "admin_name",
            "Admin"
        )
    )


# =========================================================
# ADMIN DELETE BOOKING
# =========================================================

@app.route(
    "/admin-delete-booking",
    methods=["POST"]
)
def admin_delete_booking():

    if not admin_required():

        return redirect(
            "/admin-login"
        )

    booking_id = request.form.get(
        "booking_id",
        ""
    ).strip()

    pnr = request.form.get(
        "pnr",
        ""
    ).strip()

    old_id = request.form.get(
        "id"
    )

    db = get_db_connection()

    cursor = db.cursor()

    if booking_id:

        cursor.execute("""
            DELETE FROM bookings
            WHERE booking_id = %s
        """, (
            booking_id,
        ))

    elif pnr:

        cursor.execute("""
            DELETE FROM bookings
            WHERE pnr = %s
        """, (
            pnr,
        ))

    else:

        cursor.execute("""
            DELETE FROM bookings
            WHERE id = %s
        """, (
            old_id,
        ))

    db.commit()

    cursor.close()
    db.close()

    return redirect(
        "/admin-dashboard"
    )


# =========================================================
# ADMIN USERS
# =========================================================

@app.route("/admin-users")
def admin_users():

    if not admin_required():

        return redirect(
            "/admin-login"
        )

    db = get_db_connection()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            mobile
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(

        "admin_users.html",

        users=users,

        admin_name=session.get(
            "admin_name",
            "Admin"
        )
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    import os

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )