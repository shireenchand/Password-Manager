from tkinter import *
import sqlite3
import time

root = Tk()
root.geometry("400x400")
root.title("Password Manager")

# Create a database or connect to one
conn = sqlite3.connect('passwords_book.db')

# Create cursor
c = conn.cursor()

#Create table
#
# c.execute("""CREATE TABLE passwords (
# site text,
# username text,
# password text
# )""")

# c.execute("INSERT INTO passwords VALUES (:site, :username, :password)",
#                   {
#                       'site': "SITE",
#                       'username': "USERNAME",
#                       'password': "PASSWORD"
#
#                   })


# Function to check entry password
def check():
    if entry_pass.get() == "hello":
        entry_pass.delete(0,END)
    else:
        wrong_pass = Label(root, text="Wrong Password")
        wrong_pass.grid(row=2, column=0, columnspan=2)
        entry_pass.delete(0,END)

    open_menu()

# Function to open show menu
def show():
    show_menu = Tk()
    show_menu.geometry("550x400")
    show_menu.title("Show Password")
    site_show = Entry(show_menu, width=30)
    site_show.grid(row=0, column=1, padx=10, pady=10)
    site_show_label = Label(show_menu, text="Site Name")
    site_show_label.grid(row=0, column=0)

    # Creating function to show the records
    def show_new():
        global site
        global username
        global password
        # myLabel = Label(show_menu, text="All records")
        # myLabel.grid(row=4, column=0, columnspan=2, padx=(10, 0))

        # Create a database or connect to one
        conn = sqlite3.connect('passwords_book.db')
        # Create cursor
        c = conn.cursor()

        site_asked = site_show.get()
        # Query the database
        c.execute("""SELECT *, oid FROM passwords 
        WHERE site=:site""",
                  {
                      'site': site_asked
                  })
        records = c.fetchall()
        # print(records)

        # Loop Thru Results
        i=1
        for record in records:
            site_show_label = Label(show_menu, text=record[0])
            site_show_label.grid(row=i, column=0)
            username_show_label = Label(show_menu, text=record[1])
            username_show_label.grid(row=i, column=1)
            password_show_label = Label(show_menu, text=record[2])
            password_show_label.grid(row=i, column=2)
            oid_show_label = Label(show_menu, text=record[3])
            oid_show_label.grid(row=i, column=3)
            i = i + 1

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()

        def close_func():
            show_menu.destroy()

        site_show['state']='disabled'
        show_btn['state']='disabled'
        close_btn=Button(show_menu,text="close",command=close_func)
        close_btn.grid(row=4,column=0,columnspan=2, pady=10, padx=(60, 10), ipadx=137)


    # Creating Show Button
    show_btn = Button(show_menu, text="Submit", command=show_new)
    show_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=(60, 10), ipadx=137)




# Function to open add menu
def add():


    add_menu = Tk()
    add_menu.geometry("500x400")
    add_menu.title("Add Password")
    
    # Creating Input fields
    site = Entry(add_menu, width=30)
    site.grid(row=0,column=1,padx=10,pady=10)
    username = Entry(add_menu, width=30)
    username.grid(row=1,column=1,padx=10,pady=10)
    password = Entry(add_menu,width=30)
    password.grid(row=2, column=1, padx=10, pady=10)

    # Creating Labels
    site_label = Label(add_menu, text="Site Name")
    site_label.grid(row=0,column=0)
    username_label = Label(add_menu, text="Username or Email")
    username_label.grid(row=1,column=0)
    password_label = Label(add_menu, text="Password")
    password_label.grid(row=2, column=0)

    # Function to add password to database
    def add_new():
        # myLabel = Label(add_menu, text="Added successfully")
        # myLabel.grid(row=4, column=0, columnspan=2,padx=(10,0))

        # Create a database or connect to one
        conn = sqlite3.connect('passwords_book.db')
        # Create cursor
        c = conn.cursor()

        # Insert Into Table
        c.execute("INSERT INTO passwords VALUES (:site, :username, :password)",
                  {
                      'site': site.get(),
                      'username': username.get(),
                      'password': password.get(),

                  })

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()

        # Clear The Text Boxes
        site.delete(0, END)
        username.delete(0, END)
        password.delete(0, END)

    # Creating Add Button
    add_btn = Button(add_menu, text="Add Password",command=add_new)
    add_btn.grid(row=3,column=0,columnspan=2,pady=10,padx=(60,10),ipadx=137)


def show_update():
    show_update_menu = Tk()
    show_update_menu.geometry("800x400")
    show_update_menu.title("Update Password")

    global site_edit
    global username_edit
    global password_edit



    def search():
        update_menu = Tk()
        update_menu.geometry("500x400")
        update_menu.title("Update Password")
        search_id = record_id.get()

        # Creating input fields
        site_edit = Entry(update_menu, width=30)
        site_edit.grid(row=0, column=1, padx=10, pady=10)
        username_edit = Entry(update_menu, width=30)
        username_edit.grid(row=1, column=1, padx=10, pady=10)
        password_edit = Entry(update_menu, width=30)
        password_edit.grid(row=2, column=1, padx=10, pady=10)

        # Creating Labels
        site_edit_label = Label(update_menu, text="Site Name")
        site_edit_label.grid(row=0, column=0)
        username_edit_label = Label(update_menu, text="Username or Email")
        username_edit_label.grid(row=1, column=0)
        password_edit_label = Label(update_menu, text="Password")
        password_edit_label.grid(row=2, column=0)

        # Create a database or connect to one
        conn = sqlite3.connect('passwords_book.db')
        # Create cursor
        c = conn.cursor()

        c.execute("SELECT * FROM passwords WHERE oid = " + search_id)
        records = c.fetchall()

        for record in records:
            site_edit.insert(0, record[0])
            username_edit.insert(0, record[1])
            password_edit.insert(0, record[2])

        def update():
            # Create a database or connect to one
            conn = sqlite3.connect('passwords_book.db')
            # Create cursor
            c = conn.cursor()

            search_id = record_id.get()

            c.execute("""UPDATE passwords SET
              	site = :site,
              	username = :username,
              	password = :password
              	WHERE oid = :oid""",
                      {
                          'site': site_edit.get(),
                          'username': username_edit.get(),
                          'password': password_edit.get(),
                          'oid': search_id
                      })

            # Commit Changes
            conn.commit()

            # Close Connection
            conn.close()

            update_menu.destroy()
            show_update_menu.destroy()


        # Create a Save Button To Save edited record
        edit_btn = Button(update_menu, text="Save Record",command=update)
        edit_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

    def delete_rec():
        search_id = record_id.get()
        # Create a database or connect to one
        conn = sqlite3.connect('passwords_book.db')
        # Create cursor
        c = conn.cursor()

        # Delete a record
        c.execute("DELETE from passwords WHERE oid = " + search_id)

        record_id.delete(0, END)

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()

        show_update_menu.destroy()

    record_id = Entry(show_update_menu, width=30)
    record_id.grid(row=0,column=1,columnspan=2,padx=10,pady=10,ipadx=137)
    record_id_label = Label(show_update_menu, text="Select ID")
    record_id_label.grid(row=0,column=0)
    submit_id_btn = Button(show_update_menu,text="Submit to update",command=search)
    submit_id_btn.grid(row=1,column=0,padx=10,columnspan=2)
    delete_rec_btn = Button(show_update_menu, text="Delete record", command=delete_rec)
    delete_rec_btn.grid(row=1, column=1, pady=10, padx=10,columnspan=2)


    # Create a database or connect to one
    conn = sqlite3.connect('passwords_book.db')
    # Create cursor
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *,oid FROM passwords")
    records = c.fetchall()
    # print(records)

    # Loop Thru Results
    print_records = ''
    i=2
    for record in records:
        site_show_label = Label(show_update_menu, text=record[0])
        site_show_label.grid(row=i,column=0)
        username_show_label = Label(show_update_menu,text=record[1])
        username_show_label.grid(row=i,column=1)
        password_show_label = Label(show_update_menu,text=record[2])
        password_show_label.grid(row=i,column=2)
        oid_show_label = Label(show_update_menu,text=record[3])
        oid_show_label.grid(row=i,column=3)
        i=i+1

    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()





# Creating Entry Password Buttons for main menu
entry_pass = Entry(root, width=30)
entry_pass.grid(row=0,column=1, padx=10,pady=100)
entry_pass_label = Label(root, text="Password")
entry_pass_label.grid(row=0,column=0)
submit_btn = Button(root, text="Submit", command=check)
submit_btn.grid(row=1,column=0,columnspan=2,ipadx=130)


def open_menu():
    menu = Tk()
    menu.geometry("500x400")
    menu.title("Password Manager")

    global site_name_asked
    #Creating Menu Options
    show_pass = Button(menu, text="Show Password", command=show)
    show_pass.grid(row=0,column=0,columnspan=2,padx=20,pady=(50,0), ipadx=134,sticky="nsew")
    add_pass = Button(menu, text="Add Password", command=add)
    add_pass.grid(row=1, column=0, columnspan=2, padx=20, pady=(10,0), ipadx=139,sticky="nsew")
    update_pass = Button(menu, text="Show All Passwords or Update",command=show_update)
    update_pass.grid(row=3, column=0, columnspan=2, padx=20, pady=10, ipadx=130,sticky="nsew")

#Commit Changes
conn.commit()

# Close Connection
conn.close()

root.mainloop()

