from secrets import choice
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
        
def user_input():
    while True:
        print("For creating a new post, enter 1")
        print(" ")
        print("For viewing all other posts, enter 2")
        print(" ")
        print("To exit the application, enter 3")
        print(" ")
        print("Input the number corresponding with your selection")
        choice = (input("Enter choice: "))
        try:
            if choice == ("1"):
                content=input("Enter post here: ")
                cursor.execute("INSERT INTO blog_post(username,content,id) VALUES(?,?,NULL)", [username,content])
                conn.commit()
                print("Post entered successfully!")
                print(" ")     
            elif choice == ("2"):
                print(" ")
                cursor.execute("SELECT content FROM blog_post")
                blog_list = cursor.fetchall()
                for content in blog_list:
                    print(content)
                print(" ")
            elif choice == ("3"):
                break
            else:
                raise InputError
        except InputError:
            print("Invalid input. Try again.")
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




(conn,cursor) = connect_db()
username = input("Enter your username: ")
print(" ")
user_input()
disconnect_db(conn,cursor)
print(" ")
print("You are now disconnected.")
