from tkinter import *
from tkinter import messagebox
import json
import pyperclip
from password_generator import password_generator

window_bg = "#115e31"
field_colors = "#c2c0c0"
field_font_color = "#c70039"
label_color = "black"
font = ("Comic Sans Ms", 12, "italic")

def get_password():
    password = password_generator()
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(END, password)

def database_manager(new_user_entry):
    try:
        with open("data.json", mode="r") as old_password_file:
          password_data = json.load(old_password_file)  
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open("data.json", mode="w") as new_password_file:
            json.dump(new_user_entry, new_password_file, indent=4)
    else:
        password_data.update(new_user_entry)
        with open("data.json", mode="w") as old_password_file:
            json.dump(password_data, old_password_file, indent=4)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)


def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title = "Ups!", message = "Esi atstājis tukšus laukus")
    else:
        is_ok = messagebox.askokcancel(title = "Apstiprini informāciju", message = f"Epasts: {email}" f"\nParole: {password}\nPareizi?")
        if is_ok:
            pyperclip.copy(password)
            new_entry_in_json = {
                website:
                    {
                        "Epasts": email,
                        "Parole": password
                    }
            }
            database_manager(new_entry_in_json)

def search_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Ups!", message="Ieraksti web lapu/app")
    else:
        try:
            with open("data.json", mode="r") as old_password_file:
                password_data = json.load(old_password_file)
        except(FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showinfo(title="Nav saglabātas paroles", message="Iepriekš neesi izveidojis paroli")
        else:
            if website in password_data:
                email = password_data[website]["Epasts"]
                password = password_data[website]["Parole"]
                is_clipboard = messagebox.askokcancel(title=website, message=f"Epasts/lietotājs: {email}\nParole: {password}" f"\n\nSaglabāt?")
                if is_clipboard:
                    pyperclip.copy(password)
                    messagebox.showinfo(title="Saglabāts", message="Parole ir nokopēta")
            else:
                messagebox.showinfo(title="Parole nav saglabāta", message=f"Parole {website}\n"f"nav saglabāta")

window = Tk()
window.title("Tava paroļu datubāze")
window.config(padx=20, pady=20, bg=window_bg)

website_label = Label(text="Weblapa/app", bg=window_bg, padx=20, pady=20, font=font, fg=label_color)
website_label.grid(column=0, row=1, sticky=W)

email_label = Label(text="Epasts/lietotājs", bg=window_bg, padx=20, pady=20, font=font, fg=label_color)
email_label.grid(column=0, row=2, sticky=W)

password_label = Label(text="Parole", bg=window_bg, padx=20, pady=20, font=font, fg=label_color)
password_label.grid(column=0, row=3, sticky=W)
window.grid_columnconfigure(1, weight=1)

website_entry = Entry(width=30, bg=field_colors, fg=field_font_color, font=font)
website_entry.insert(END, string="")
website_entry.grid(column=1, row=1)

website_entry.focus()

email_entry = Entry(width=30, bg=field_colors, fg=field_font_color, font=font)
email_entry.insert(END, string="")
email_entry.grid(column=1, row=2)

password_entry = Entry(width=30, bg=field_colors, fg=field_font_color, font=font)
password_entry.insert(END, string="")
password_entry.grid(column=1, row=3)

search_button = Button(text="Meklēt", padx=95, font=font, command=search_password, bg='#d67a40')
search_button.grid(column=3, row=1)

generate_button = Button(text="Veidot paroli", command = get_password, font=font, bg='#d67a40')
generate_button.grid(column=3, row=3)

add_button = Button(text = "Pievienot", width=36, command=save_password, font=font, bg='#d67a40')
add_button.grid(column=1, row=5, columnspan=2, sticky=W)

dummy_label = Label(bg=window_bg)
dummy_label.grid(column=0, row=4, sticky=W)

window.mainloop()


