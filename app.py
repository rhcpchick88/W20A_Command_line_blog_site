from asyncio import exceptions
from logging import exception
from dbcreds import *
import mariadb

class InputError(Exception):
    pass

def connect_db():
    conn=None
    cursor=None
    
    try:
        conn=mariadb.connect(host=host, port=port, user=user, password=password, database=database)
        cursor=conn.cursor()
        print("you have successfully connected to the database")
        return(conn,cursor)
    
    except mariadb.OperationalError as e:
        print("Got an operational error")
        if ("Access denied" in e.msg):
            print("Failed to log in")
        disconnect_db(conn,cursor)
        
def disconnect_db(conn,cursor):
    if (cursor != None):
        cursor.close()
    if (conn != None):
        conn.rollback()
        conn.close()
        
def post_options():
    try:
        (conn,cursor) = connect_db()
        print("You are now connected!")
        print("For creating a new post, enter 1")
        print("For viewing all other posts, enter 2")
        choice = input("Input the number corresponding with your selection")
        (input("Enter choice: "))
        while True:
            try:
                if choice == ("1"):
                    enter_blogpost()
                elif choice == ("2"):
                    view_blogposts()
                else:
                    raise InputError
            except InputError:
                print("Invalid input. Try again.")
            else:
                break
    except mariadb.IntegrityError as e:
        print("Integrity error")
        print(e.msg)
    except mariadb.ProgrammingError as e:
        if ("SQL syntax" in e.msg):
            print("Programming error")
            print(e.msg)
    finally:
        disconnect_db(conn,cursor)                    
    
def insert_username():
    try:
        (conn,cursor) = connect_db()
        username = input("Enter your username: ")
        cursor.execute("INSERT INTO blog_post(username) VALUES(?)", [username])
        while True:
            try:    
                if(cursor.rowcount == 1):
                    conn.commit()
                    print("username entered successfully")
                else:
                    raise InputError
            except InputError:
                print("Invalid input, please try again")
            else:
                break
        post_options()
    except mariadb.OperationalError as e:
        print("Got an operational error")
        if ("Access Denied" in e.msg):
            print("Failed to log in")
    except mariadb.IntegrityError as e:
        print("Integrity error")
        print(e.msg)
    except mariadb.ProgrammingError as e:
        if ("SQL syntax" in e.msg):
            print("Programming error")
            print(e.msg)
    finally:
        disconnect_db(conn,cursor)

insert_username()
    
    
