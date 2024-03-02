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
          user='dpasha',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='dpashapw',
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

def view_all_beyblades():
    """
    """

def view_all_battle_results_for_user():
    """
    """

def view_battle_results_for_tournament():
    """
    """

def view_battle_results_for_date():
    """
    """

def view_battle_results_for_location():
    """
    """

def get_beyblade_name_and_heav_weight_for_type():
    """
    """

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
    Checks the `is_client` flag for the given username in the `users` table.
    """
    cursor = conn.cursor()
    sql = "SELECT is_client FROM users WHERE username = %s;"
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
    print('  (a) - View All Beyblades')
    # Add more options as needed
    print('  (b) - View your battle results')
    print('  (c) - View battle results for a tournament')
    print('  (d) - View battle results for specific date')
    print('  (e) - View battle results for location')
    print('  (f) - Get the name and weight of the heaviest Beyblade for a Type')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()

    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        print("VIEWING ALL BEYBLADES.")
        view_all_beyblades()
        show_options()
    elif ans == 'b':
        print("VIEWING ALL BATTLE RESULTS FOR USER.")
        view_all_battle_results_for_user()
        show_options()
    elif ans == 'c':
        print("VIEWING ALL BATTLE RESULTS FOR TOURNAMENT.")
        view_battle_results_for_tournament()
        show_options()
    elif ans == 'd':
        print("VIEWING ALL BATTLE RESULTS FOR DATE.")
        view_battle_results_for_date()
        show_options()
    elif ans == 'e':
        print("VIEWING ALL BATTLE RESULTS FOR LOCATION.")
        view_battle_results_for_location()
        show_options()
    elif ans == 'f':
        print("RETRIEVING HEAVIEST BEYBLADE.")
        get_beyblade_name_and_heav_weight_for_type()
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
