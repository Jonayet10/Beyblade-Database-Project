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
          database='beybladedb' # replace this with your database name
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
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
    sql = ("INSERT INTO battles (tournament_name, date, location, player1_id, player2_id, player1_beyblade_id, player2_beyblade_id, winner_id) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    data = (tournament_name, date, location, player1_id, player2_id, player1_beyblade_id, player2_beyblade_id, winner_id)
    try:
        cursor.execute(sql, data)
        conn.commit()
        print("New battle result added successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)

def is_admin(username):
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

        while not is_admin(username):
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
    print('  (a) - Add a new Beyblade')
    print('  (b) - Add a new battle result')
    # Add more options as needed
    print('  (q) - quit')
    print()
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
