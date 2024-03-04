"""
Student name(s): Jonayet Lavin, Alina Zhang, Deepro Pasha

Student email(s): jlavin@caltech.edu, alinazhang@caltech.edu, dpasha@caltech.edu

Clients (Beybladers) can view battle information and results in the 'battles'
table and can view Beyblades in the 'beyblades' table. 

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
          user='gokus',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='gokuspw',
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

    # Closing cursor and connection
    cursor.close()
    conn.close()

    return results

def view_all_battle_results_for_user(user_name):
    """
    Queries the battles table for all battle results related to the 
    current user. 

    Arguments:
        user_name (str) - the name of the user. 

    Return value: Query of the battles table. 
    """

def view_battle_results_for_tournament(tournament_name):
    """
    Queries the battles table for all battle results related to the 
    specified tournament. 

    Arguments:
        tournament_name (str) - the name of the tournament.  

    Return value: Query of the battles table. 
    """

def view_battle_results_for_location(location):
    """
    Queries the battles table for all battle results related to the 
    specified location. 

    Arguments:
        location (str) - the specified location.

    Return value: Query of the battles table.
    """

def view_beyblade_info(name):
    """
    Queries the beyblades table for the information of all beyblades with that
    particular name.

    Arguments:
        name (str) - the specified beyblade name.

    Return value: Query of the beyblades table. 
    """

def view_part_info(part_name):
    """
    Queries the parts table for the information of the specified part name.

    Arguments:
        part_name (str) - the specified part name.

    Return value: Query of the parts table. 
    """

def view_user_beyblades(user_name):
    """
    Queries the userbeyblades table for the beyblades of the specified user 
    name.

    Arguments:
        user_name (str) - the specified user name.

    Return value: Query of the userbeyblades table.  
    """

def add_beyblade(name, type, series, is_custom, face_bolt_id, energy_ring_id, 
                 fusion_wheel_id, spin_track_id, performance_tip_id):
    """
    Adds the beyblade to the beyblades and userbeyblades table.

    Arguments:
        name (str) ... (so on.) TODO
    
    Return value: none.
    """
    conn = get_conn()
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



# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)

def is_client(username):
    """
    Helper function to verify whether the user logging in is a BeyClient.
    Checks the `is_admin` flag for the given username in the `users` table.
    """
    cursor = conn.cursor()
    sql = "SELECT is_admin FROM users WHERE username = %s;"
    try:
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        # If the user exists and the is_admin flag is false, return True
        if result and (not result[0]):
            return False
        else:
            return True
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

    print("\n------------------------------ BeyClient Login ------------------------------\n")

    while True:
        username = input("USERNAME: ").lower()
        password = input("PASSWORD: ").lower()

        while not is_client(username):
            print("\nIt appears that you are not a BeyClient. Please try again! \n")
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
def add_user(username, email, password, is_client):
    """
    Adds the user to the users and user_info table.

    Arguments:
        username (str) - TODO
        email (str) - TODO
        password (str) - TODO
        is_client (bool) - TODO
    
    Return value: none.
    """
    cursor = conn.cursor()
    sql_user_info = "CALL sp_add_user(%s, %s)"  # Call the stored procedure to add user to user_info table
    sql_users = "INSERT INTO users (username, email, is_admin) VALUES (%s, %s, %s)"  # Add user to users table
    try:
        # Add user to user_info table
        cursor.execute(sql_user_info, (username, password))
        # Add user to users table
        cursor.execute(sql_users, (username, email, is_client))
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
    # Add more options as needed
    print('  (a) - View all Beyblades')
    print('  (b) - View your battle results')
    print('  (c) - View battle results for a tournament')
    print('  (d) - View battle results for location')
    print('  (e) - View information about a Beyblade.')
    print('  (f) - View information about a part.')
    print('  (g) - View your Beyblades.')
    print('  (h) - Add a Beyblade.')
    print('  (i) - Add a user.')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()

    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        print("VIEWING ALL BEYBLADES.")
        print(view_all_beyblades())
        show_options()
    elif ans == 'b':
        print("VIEWING ALL BATTLE RESULTS FOR USER.")
        # view_all_battle_results_for_user()
        show_options()
    elif ans == 'c':
        print("VIEWING ALL BATTLE RESULTS FOR TOURNAMENT.")
        # view_battle_results_for_tournament()
        show_options()
    elif ans == 'd':
        print("VIEWING ALL BATTLE RESULTS FOR LOCATION.")
        # view_battle_results_for_location()
        show_options()
    elif ans == 'e':
        print("VIEWING INFORMATION ABOUT A BEYBLADE.")
        # view_beyblade_info()
        show_options()
    elif ans == 'f':
        print("VIEWING INFORMATION ABOUT A PART.")
        # view_part_info()
        show_options()
    elif ans == 'g':
        print("VIEWING ALL USER BEYBLADES.")
        # view_user_beyblades()
        show_options()
    elif ans == 'h':
        # Prompt for Beyblade details and call add_beyblade function
        # TODO: Fix style here, keep it under 80 chars per line. 
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
    elif ans == 'i':
        # Prompt for user details and call a function to add the user
        # TODO: Fix style here, keep it under 80 chars per line. 
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = input('Enter password: ')
        user_input = input('Is the user an admin? (True/False): ').lower()
        is_client = user_input not in ['true', '1', 't', 'y', 'yes']

        add_user(username, email, password, is_client)
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
