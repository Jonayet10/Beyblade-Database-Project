"""
Student name(s): Jonayet Lavin, Alina Zhang, Deepro Pasha

Student email(s): jlavin@caltech.edu, alinazhang@caltech.edu, dpasha@caltech.edu

Admins (BeyMasters) can add battle information and results to the 'battles' table,
and add Beyblades to 'beyblades' table, custom or stock.

"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
from tabulate import tabulate

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='jlavin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='jlavinpw',
          database='beybladedb', # replace this with your database name
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr.write('Incorrect username or password when connecting to DB.' + '\n')
            sys.stderr.flush()
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr.write('Database does not exist.' + '\n')
            sys.stderr.flush()
        elif DEBUG:
            sys.stderr.write(str(err) + '\n')
            sys.stderr.flush()

        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------

def add_beyblade(name, type, series, is_custom, face_bolt_id, energy_ring_id, fusion_wheel_id, spin_track_id, performance_tip_id):
    cursor = conn.cursor()
    sql = ("INSERT INTO beyblades (name, type, series, is_custom, face_bolt_id, energy_ring_id, fusion_wheel_id, spin_track_id, performance_tip_id) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data = (name, type, series, is_custom, face_bolt_id, energy_ring_id, fusion_wheel_id, spin_track_id, performance_tip_id)
    try:
        cursor.execute(sql, data)
        conn.commit()
        print(f"Added new Beyblade: {name}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def add_battle(tournament_name, date, location, player1_id, player2_id, player1_beyblade_id, player2_beyblade_id, winner_id):
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_record_battle', (tournament_name, date, location, player1_id, player2_id, player1_beyblade_id, player2_beyblade_id, winner_id))
        conn.commit()
        print("New battle result added successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        
def view_users():
    """
    Retrieves and displays a list of all users and their information.
    """
    cursor = conn.cursor()
    sql = "SELECT user_ID, username, email, is_admin, date_joined FROM users;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            print("\nCurrent Users:")
            print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Admin':<10} {'Date Joined'}")
            for row in results:
                user_id, username, email, is_admin, date_joined = row
                admin_status = "Yes" if is_admin else "No"
                print(f"{user_id:<5} {username:<20} {email:<30} {admin_status:<10} {date_joined}")
        else:
            print("No users found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# -------------------------------------------- Functions that also the client has ---------------------------------------------------
def view_all_beyblades():
    """
    Queries the beyblades table for 
    the entirety of all beyblades for the user to look through. 

    Return value: Query of the beyblades table.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM beyblades;")

    # Fetching all results
    results = cursor.fetchall()

    # Defining the table headers as per beyblades table columns
    headers = ['Beyblade ID', 'Name', 'Type', 'Is Custom', 'Series', 
               'Face Bolt ID', 'Energy Ring ID', 'Fusion Wheel ID', 
               'Spin Track ID', 'Performance Tip ID']

    # Printing the results in a table format
    print(tabulate(results, headers=headers, tablefmt="grid"))

    # Closing cursor and connection
    cursor.close()
    conn.close()

def view_all_battle_results_for_user(user_name):
    """
    Queries the battles table for all battle results related to the 
    current user. 

    Arguments:
        user_name (str) - the name of the user. 

    Return value: Query of the battles table. 
    """
    conn = get_conn()
    cursor = conn.cursor()

    # SQL query to fetch battle results for the given user
    query = """
    SELECT b.battle_ID, b.tournament_name, b.date, b.location, 
           u1.username AS Player1_Username, u2.username AS Player2_Username, 
           bb1.name AS Player1_Beyblade_Name, bb2.name AS Player2_Beyblade_Name, 
           b.player1_beyblade_ID, b.player2_beyblade_ID, b.winner_ID
    FROM battles b
    JOIN users u1 ON b.player1_ID = u1.user_ID
    JOIN users u2 ON b.player2_ID = u2.user_ID
    JOIN userbeyblades ub1 ON b.player1_beyblade_ID = ub1.user_beyblade_ID
    JOIN beyblades bb1 ON ub1.beyblade_ID = bb1.beyblade_ID
    JOIN userbeyblades ub2 ON b.player2_beyblade_ID = ub2.user_beyblade_ID
    JOIN beyblades bb2 ON ub2.beyblade_ID = bb2.beyblade_ID
    WHERE u1.username = %s OR u2.username = %s;
    """
    cursor.execute(query, (user_name, user_name))

    # Fetching all results
    results = cursor.fetchall()
    headers = ["Battle ID", "Tournament Name", "Date", "Location", 
               "Player 1 Username", "Player 2 Username", 
               "Player 1 Beyblade Name", "Player 2 Beyblade Name", 
               "Player 1 Beyblade ID", "Player 2 BeyBlade ID", "Winner ID"]
    
    print(tabulate(results, headers=headers, tablefmt="grid"))
    # Closing cursor and connection
    cursor.close()
    conn.close()

def view_battle_results_for_tournament(tournament_name):
    """
    Queries the battles table for all battle results related to the specified tournament.
    
    Arguments:
        tournament_name (str) - the name of the tournament.

    Return value: None. Prints the query result of the battles table in a formatted table.
    """
    conn = get_conn()
    cursor = conn.cursor()

    # SQL query to fetch battle results for the given tournament name
    query = """
    SELECT b.battle_ID, b.date, b.location, 
           u1.username AS Player1_Username, u2.username AS Player2_Username, 
           bb1.name AS Player1_Beyblade_Name, bb2.name AS Player2_Beyblade_Name, 
           b.player1_beyblade_ID, b.player2_beyblade_ID, b.winner_ID
    FROM battles b
    JOIN users u1 ON b.player1_ID = u1.user_ID
    JOIN users u2 ON b.player2_ID = u2.user_ID
    JOIN userbeyblades ub1 ON b.player1_beyblade_ID = ub1.user_beyblade_ID
    JOIN beyblades bb1 ON ub1.beyblade_ID = bb1.beyblade_ID
    JOIN userbeyblades ub2 ON b.player2_beyblade_ID = ub2.user_beyblade_ID
    JOIN beyblades bb2 ON ub2.beyblade_ID = bb2.beyblade_ID
    WHERE b.tournament_name = %s;
    """
    cursor.execute(query, (tournament_name,))

    # Fetching all results
    results = cursor.fetchall()
    headers = ["Battle ID", "Date", "Location", 
               "Player 1 Username", "Player 2 Username", 
               "Player 1 Beyblade Name", "Player 2 Beyblade Name", 
               "Player 1 Beyblade ID", "Player 2 BeyBlade ID", "Winner ID"]
    
    # Check if there are any results
    if results:
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print(f"No battles found for tournament: {tournament_name}")

    # Closing cursor and connection
    cursor.close()
    conn.close()

def view_battle_results_for_location(location):
    """
    Queries the battles table for all battle results related to the specified location.
    
    Arguments:
        location (str) - the specified location of the battles to query.

    Return value: None. Prints the query result of the battles table in a formatted table.
    """
    conn = get_conn()
    cursor = conn.cursor()

    # SQL query to fetch battle results for the given location
    query = """
    SELECT b.battle_ID, b.tournament_name, b.date, 
           u1.username AS Player1_Username, u2.username AS Player2_Username, 
           bb1.name AS Player1_Beyblade_Name, bb2.name AS Player2_Beyblade_Name, 
           b.player1_beyblade_ID, b.player2_beyblade_ID, b.winner_ID
    FROM battles b
    JOIN users u1 ON b.player1_ID = u1.user_ID
    JOIN users u2 ON b.player2_ID = u2.user_ID
    JOIN userbeyblades ub1 ON b.player1_beyblade_ID = ub1.user_beyblade_ID
    JOIN beyblades bb1 ON ub1.beyblade_ID = bb1.beyblade_ID
    JOIN userbeyblades ub2 ON b.player2_beyblade_ID = ub2.user_beyblade_ID
    JOIN beyblades bb2 ON ub2.beyblade_ID = bb2.beyblade_ID
    WHERE b.location = %s;
    """
    cursor.execute(query, (location,))

    # Fetching all results
    results = cursor.fetchall()
    headers = ["Battle ID", "Tournament Name", "Date", 
               "Player 1 Username", "Player 2 Username", 
               "Player 1 Beyblade Name", "Player 2 Beyblade Name", 
               "Player 1 Beyblade ID", "Player 2 BeyBlade ID", "Winner ID"]
    
    # Check if there are any results
    if results:
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print(f"No battles found for location: {location}")

    # Closing cursor and connection
    cursor.close()
    conn.close()


def view_part_info(part_id):
    """
    Queries the parts table for information about a specific part given its part_ID.
    
    Arguments:
        part_id (str) - the unique identifier for the part to query.

    Return value: None. Prints the query result of the part in a formatted table.
    """
    conn = get_conn()
    cursor = conn.cursor()

    # SQL query to fetch information for the given part_ID
    query = """
    SELECT part_ID, part_type, weight, description
    FROM parts
    WHERE part_ID = %s;
    """
    cursor.execute(query, (part_id,))

    # Fetching the result
    result = cursor.fetchone()
    
    headers = ["Part ID", "Part Type", "Weight", "Description"]
    
    # Check if there is a result
    if result:
        print(tabulate([result], headers=headers, tablefmt="grid"))
    else:
        print(f"No information found for part ID: {part_id}")

    # Closing cursor and connection
    cursor.close()
    conn.close()


def view_user_beyblades(user_name):
    """
    Queries the database for all Beyblades owned by a specific user and prints
    their beyblade_ID and name in a well-formatted table.
    
    Arguments:
        user_name (str) - The username of the user.
    Returns: Prints the Beyblade ID and Name of the user's Beyblades
    """
    conn = get_conn()
    cursor = conn.cursor()

    query = """
    SELECT b.beyblade_ID, b.name
    FROM beyblades b
    JOIN userbeyblades ub ON b.beyblade_ID = ub.beyblade_ID
    JOIN users u ON ub.user_ID = u.user_ID
    WHERE u.username = %s;
    """
    cursor.execute(query, (user_name,))

    results = cursor.fetchall()
    headers = ["Beyblade ID", "Name"]

    if results:
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print(f"No Beyblades found for user: {user_name}")

    cursor.close()
    conn.close()

def view_beyblade_parts(beyblade_id):
    """
    Queries the database for the names and weights of all parts that make up a specific
    Beyblade and prints them in a well-formatted table.
    
    Arguments:
        beyblade_id (str) - The ID of the Beyblade.
    Returns: Prints the PART ID, Part Type, Part Description, and Weight in a formatted table.
    """
    conn = get_conn()
    cursor = conn.cursor()

    query = """
    SELECT p.part_ID, p.part_type, p.weight, p.description
    FROM parts p
    JOIN beyblades b ON p.part_ID IN (b.face_bolt_ID, b.energy_ring_ID, 
                                      b.fusion_wheel_ID, b.spin_track_ID, 
                                      b.performance_tip_ID)
    WHERE b.beyblade_ID = %s;
    """
    cursor.execute(query, (beyblade_id,))

    results = cursor.fetchall()
    headers = ["Part ID", "Part Type", "Weight (g)", "Description"]

    if results:
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print(f"No parts found for Beyblade ID: {beyblade_id}")

    cursor.close()
    conn.close()

def add_user_beyblade(name, type, series, face_bolt_id, energy_ring_id, 
                 fusion_wheel_id, spin_track_id, performance_tip_id):
    """
    Adds the beyblade to the beyblades and userbeyblades table.

    Arguments:
        name (str) ... (so on.) TODO
    
    Return value: none.
    """
    cursor = conn.cursor()
    sql = ("CALL sp_add_beyblade(%s, %s, %s, %s, %s, %s, %s, %s)")
    data = (name, type, series, face_bolt_id, energy_ring_id, fusion_wheel_id, spin_track_id, performance_tip_id)
    try:
        cursor.execute(sql, data)
        conn.commit()
        print(f"Added new Beyblade: {name}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def udf_heaviest_beyblade_for_type(beyblade_type):
    """
    Fetches and displays the ID and name of the heaviest Beyblade of a specific type.
    Arguments:
        beyblade_type (str): The type of Beyblade (Attack, Defense, Stamina, Balance).
    """
    conn = get_conn()
    cursor = conn.cursor()

    # Call the UDF `get_heaviest_beyblade_id` passing the beyblade type
    query = f"SELECT get_heaviest_beyblade_id('{beyblade_type}') AS heaviest_beyblade_id;"
    cursor.execute(query)

    # Fetching the result which is the ID of the heaviest beyblade
    result = cursor.fetchone()
    if result and result[0]:
        beyblade_id = result[0]
        # Fetch beyblade name using the ID
        cursor.execute("SELECT name FROM beyblades WHERE beyblade_id = %s;", (beyblade_id,))
        name_result = cursor.fetchone()
        if name_result and name_result[0]:
            print(f"The heaviest Beyblade of type '{beyblade_type}' is ID: {beyblade_id}, Name: {name_result[0]}")
        else:
            print(f"No Beyblade found with ID: {beyblade_id}")
    else:
        print(f"No heaviest Beyblade found for type '{beyblade_type}'.")

    cursor.close()
    conn.close()

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)

def is_admin_func(username):
    """
    Helper function to verify whether the user logging in is a BeyAdmin.
    Checks the `is_admin` flag for the given username in the `users` table.
    """
    cursor = conn.cursor()
    sql = "SELECT is_admin FROM users WHERE username = %s;"
    try:
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        # If the user exists and the is_admin flag is True, return True
        if result and result[0]:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    finally:
        cursor.close()

def login():
    """
    This function prompts the login for an admin.
    It checks the database to ensure that the username and password are correct.
    """
    cursor = conn.cursor()

    print("\n------------------------------ BeyAdmin Login ------------------------------\n")

    while True:
        username = input("USERNAME: ").lower()
        password = input("PASSWORD: ").lower()

        while not is_admin_func(username):
            print("\nIt appears that you are not a BeyAdmin. Please try again! \n")
            username = input("USERNAME: ").lower()
            password = input("PASSWORD: ").lower()

        sql = "SELECT authenticate('%s', '%s');" % (username, password)

        try:
            cursor.execute(sql)
            check_response = cursor.fetchone()

            if check_response[0] == 1:
                show_options()
            else:
                print("\nUsername or password is incorrect. Please try again :)\n")

        except mysql.connector.Error as err:
            if DEBUG:
                sys.stderr(err)
                sys.exit(1)
            else:
                sys.stderr("Error logging in.")

# Add user to 'user_info' and 'users' tables
def add_user(username, email, password, is_admin):
    cursor = conn.cursor()
    sql_user_info = "CALL sp_add_user(%s, %s, %s)"  # Call the stored procedure to add user to user_info table
    sql_users = "INSERT INTO users (username, email, is_admin) VALUES (%s, %s, %s)"  # Add user to users table
    try:
        # Add user to user_info table
        cursor.execute(sql_user_info, (username, password, is_admin))
        # Add user to users table
        cursor.execute(sql_users, (username, email, is_admin))
        conn.commit()
        print(f"User '{username}' added successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    
    print('  (a) - Add a new Beyblade to database')
    print('  (b) - Add a new battle result')
    print('  (c) - Add a new user')
    print('  (d) - View current users')
    print('\n')

    print('  (e) - View all Beyblades')
    print('  (f) - View a user\'s battle results')
    print('  (g) - View battle results for a tournament')
    print('  (h) - View battle results for location')
    print('\n')

    print('  (i) - View part information')
    print('  (j) - View Beyblade ID and Name of user\'s Beyblades')
    print('  (k) - View parts of a Beyblade')
    print('  (l) - Add a Beyblade to your account')
    print('\n')

    print('  (m) - View the heaviest Beyblade by type')

    # Add more options as needed
    print('  (q) - quit')
    ans = input('Enter an option: ').lower()

    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        # Prompt for Beyblade details and call add_beyblade function
        name = input('Enter Beyblade name: ')
        type = input('Enter Beyblade type (Attack, Defense, Stamina, Balance): ')
        series = input('Enter Beyblade series (Metal Fusion, Metal Masters, Metal Fury): ')
        is_custom = input('Is it custom? (True/False): ').lower() in ['true', '1', 't', 'y', 'yes']
        face_bolt_id = input('Enter Face Bolt ID: ')
        energy_ring_id = input('Enter Energy Ring ID: ')
        fusion_wheel_id = input('Enter Fusion Wheel ID: ')
        spin_track_id = input('Enter Spin Track ID: ')
        performance_tip_id = input('Enter Performance Tip ID: ')
        add_beyblade(name, type, series, is_custom, face_bolt_id, energy_ring_id, fusion_wheel_id, spin_track_id, performance_tip_id)
        show_options()
    elif ans == 'b':
        # Prompt for battle details and call a function to add battle result
        tournament_name = input('Enter tournament name: ')
        date = input('Enter date of the battle (YYYY-MM-DD HH:MM:SS): ')
        location = input('Enter location: ')
        player1_id = input('Enter Player 1 ID: ')
        player2_id = input('Enter Player 2 ID: ')
        player1_beyblade_id = input('Enter Player 1 Beyblade ID: ')
        player2_beyblade_id = input('Enter Player 2 Beyblade ID: ')
        winner_id = input('Enter Winner ID (leave blank if draw): ')
        winner_id = winner_id if winner_id.strip() != '' else None
        add_battle(tournament_name, date, location, player1_id, player2_id, player1_beyblade_id, player2_beyblade_id, winner_id)
        show_options()
    elif ans == 'c':
        # Prompt for user details and call a function to add the user
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = input('Enter password: ')
        is_admin = input('Is the user an admin? (True/False): ').lower() in ['true', '1', 't', 'y', 'yes']
        add_user(username, email, password, is_admin)
        show_options()
    elif ans == 'd':
        view_users()
        show_options()
    elif ans == 'e':
        view_all_beyblades()
        show_options()
    elif ans == 'f':
        username = input('Enter username: ')
        view_all_battle_results_for_user(username)
        show_options()
    elif ans == 'g':
        tournament_name = input('Enter tournament name: ')
        view_battle_results_for_tournament(tournament_name)
        show_options()
    elif ans == 'h':
        tournament_location = input('Enter tournament location: ')
        view_all_battle_results_for_user(tournament_location)
        show_options()
    elif ans == 'i':
        part_ID = input('Enter part ID: ')
        view_part_info(part_ID)
        show_options()
    elif ans == 'j':
        user_name = input('Enter username: ')
        view_user_beyblades(user_name)
        show_options()
    elif ans == 'k':
        beyblade_ID = input('Enter Beyblade ID: ')
        view_beyblade_parts(beyblade_ID)
        show_options()
    elif ans == 'l':
        name = input('Enter Beyblade name: ')
        type = input('Enter Beyblade type (Attack, Defense, Stamina, Balance): ')
        series = input('Enter Beyblade series (Metal Fusion, Metal Masters, Metal Fury): ')
        is_custom = input('Is it custom? (True/False): ').lower() in ['true', '1', 't', 'y', 'yes']
        face_bolt_id = input('Enter Face Bolt ID: ')
        energy_ring_id = input('Enter Energy Ring ID: ')
        fusion_wheel_id = input('Enter Fusion Wheel ID: ')
        spin_track_id = input('Enter Spin Track ID: ')
        performance_tip_id = input('Enter Performance Tip ID: ')
        add_user_beyblade(name, type, series, is_custom, face_bolt_id, energy_ring_id, fusion_wheel_id, spin_track_id, performance_tip_id)
    elif ans == 'm':
        beyblade_type = input('Enter Beyblade type (Attack, Defense, Stamina, Balance): ')
        udf_heaviest_beyblade_for_type(beyblade_type)
        show_options()
    elif ans == 'q':
        quit_ui() 

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('\n----------------------------------------------------------------\n')
    print('Thank you for keeping the Beyblade legacy ablaze. May the Beyblade spirit be with you. Goodbye!')
    print('\n----------------------------------------------------------------\n')
    exit()


def main():
    """
    Main function for starting things up.
    """
    login()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
