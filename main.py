from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import random
import pyperclip
import json
small_alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
capital_alphabets = [alphabet.upper() for alphabet in small_alphabets]
numbers = ['1','2','3','4','5','6','7','8','9','0']
special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', '{', ']', '}', '\\', '|', ';', ':', '\'', '\"', ',', '<', '.', '>', '/', '?', '`', '~']
#-------------------------------------------Password Generator-----------------------------------------------
def password_button_action():
    password_entry.delete(0, END)
    generated_password = []
    for i in range(5):
        generated_password.append(random.choice(small_alphabets))
    for i in range(5):
        generated_password.append(random.choice(special_characters))
    for i in range(5):
        generated_password.append(random.choice(numbers))
    for i in range(5):
        generated_password.append(random.choice(capital_alphabets))
    random.shuffle(generated_password)
    generated_password = ''.join(generated_password)
    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)
    messagebox.showinfo(title='Password copied', message=f'Password copied to clipboard')
#-------------------------------------------Password Saving--------------------------------------------------
def add_button_action():
    website_name = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    pyperclip.copy(password)
    data_dict = {
        website_name : {
            "email" : email,
            "password" : password
        }
    }
    is_okay = True
    if len(website_name) == 0 or len(password) == 0 or len(email) == 0:
        is_okay = messagebox.askokcancel(title='Empty fields', message='One or more fields are empty are sure you want'
                                                                       ' to continue?')
    is_ok = True
    if is_okay is True:
        is_ok = messagebox.askokcancel(title=website_name, message=f"These are the details entered"
                                                                   f"\nEmail: {email}\nPassword:"
                                                                   f" {password}\nAre you sure you want to save?")
    if is_ok and is_okay:
        try:
            with open('data.json', 'r') as data_file:
                old_data = json.load(data_file)
                old_data.update(data_dict)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(data_dict, data_file, indent=4)
        else:
            with open('data.json', 'w') as data_file:
                json.dump(old_data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
#------------------------------------------Search-----------------------------------------------------------
def search_button_action():
    query = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            all_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title='NO DATA', message='THERE IS NO DATA')
    else:
        try:
            query_password = all_data[query]["password"]
            query_email = all_data[query]["email"]
        except KeyError:
            messagebox.showerror(title='Wrong query', message='You are searching for query that is not present')
        else:
            messagebox.showinfo(title=query, message=f"Email : {query_email}\nPassword : {query_password}")
            pyperclip.copy(query_password)
#-------------------------------------------UI setup---------------------------------------------------------
my_window = Tk()
my_window.title('Local Pass')
my_window.config(pady=40, padx=40)

icon_canvas = Canvas(height=200, width=200, highlightthickness=0)
icon_image = ImageTk.PhotoImage(Image.open('icon.png'))
image_edit = icon_canvas.create_image(100, 100, image=icon_image)
icon_canvas.grid(row=0, column=1, padx=(20,20), pady=(20,20))

website_label = Label(text='Website:')
website_label.grid(row=1, column=0)

email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)

password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

website_entry = Entry(width=30)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=39)
email_entry.insert(0, 'madhumaddini@gmail.com')
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=39)
password_entry.grid(row=3, column=1, columnspan=2)

password_button = Button(text='Generate Password', command=password_button_action)
password_button.grid(row=3, column=3)

add_button = Button(text='Add', width=36, command=add_button_action)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text= 'Search', command=search_button_action)
search_button.grid(row=1, column=2)

my_window.mainloop()

