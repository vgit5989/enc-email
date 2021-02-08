from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Treeview

import index_gui

def auth_pw():
    global pw_verify
    global ID
    #e_verify.get()
    c = index_gui.signin(e_verify.get(), pw_verify.get())

    if(c == 2):
        Label(sign_in_screen, text="Password", fg="red", font=("calibri", 15)).pack()
        open_body_screen.after(1500, open_body_screen.destroy())
        open_body()
        return

    body = index_gui.view_body(e_verify.get(), pw_verify.get(), ID)

    Label(open_body_screen, text="Body:").pack()

    T = Text(open_body_screen, height=40, width=60)
    T.pack()
    T.insert(END, body)
    Label(open_body_screen, text=body).pack()


def open_body(a):
    global open_body_screen
    open_body_screen = Toplevel(view_mail_screen)
    open_body_screen.title("Neutronmail - View Body")
    open_body_screen.geometry("650x350")

    Label(open_body_screen, text="Please enter details below to Sign in:").pack()
    Label(open_body_screen, text="").pack()

    global pw_verify
    pw_verify = StringVar()

    Label(open_body_screen, text="").pack()
    Label(open_body_screen, text="Renter Password for secondary verification: ").pack()
    password_sign_in_entry = Entry(open_body_screen, textvariable=pw_verify, show='*')
    password_sign_in_entry.pack()
    Label(open_body_screen, text="").pack()

    Button(open_body_screen, text="Sign In", width=10, height=1, command=auth_pw).pack()

def selectId(a):
    global ID
    curItem = router_tree_view.focus()
    ID = router_tree_view.item(curItem)['values'][0]

def view_mail():
    global view_mail_screen
    global e_verify
    global router_tree_view

    #email_action_screen
    view_mail_screen = Toplevel(email_action_screen)
    view_mail_screen.title("Neutronmail - View Email")
    view_mail_screen.geometry("650x350")

    Label(view_mail_screen, text="Inbox", padx=100, pady=20).grid(row=0, column=1, sticky=N, )

    view_tab = index_gui.view(e_verify.get())

    frame_router = Frame(view_mail_screen)
    frame_router.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

    columns = ['id', 'From', 'To', 'Subject']
    router_tree_view = Treeview(frame_router, columns=columns, show="headings")
    router_tree_view.column("id", width=30)
    for col in columns[1:3]:
        router_tree_view.column(col, width=150)
    for col in columns:
        router_tree_view.heading(col, text=col)
    router_tree_view.column("Subject", width=250)
    router_tree_view.bind('<Double-1>', open_body)
    router_tree_view.bind('<ButtonRelease-1>', selectId)
    router_tree_view.pack(side="left", fill="y")
    scrollbar = Scrollbar(frame_router, orient='vertical')
    scrollbar.configure(command=router_tree_view.yview)
    scrollbar.pack(side="right", fill="y")
    router_tree_view.config(yscrollcommand=scrollbar.set)


    for row in view_tab:
        router_tree_view.insert('', 'end', values=row)
        '''
            e = Entry(view_mail_screen, width=25, fg='blue')
            e.grid(row=i, column=j, padx=10, pady=15)
            e.insert(END, inbox[j])
            e.config(state='disabled')
            i = i + 1
        '''


def send_mail():
    c = index_gui.compose_email(email.get(), to.get(), sub.get(), body.get('1.0', END))

    if (c == 2):
        Label(email_action_screen, text="Invalid Email", fg="red", font=("calibri", 15)).pack()
        comp_mail_screen.after(500, comp_mail_screen.destroy())
        sign_in()
    else:
        Label(email_action_screen, text="Email Successfully sent!", fg="green", font=("calibri", 15)).pack()
        comp_mail_screen.after(500, comp_mail_screen.destroy())


def comp_mail():
    global comp_mail_screen
    global email
    global to
    global sub
    global body
    global e_verify

    email = StringVar()
    email.set(e_verify.get())
    del e_verify

    comp_mail_screen = Toplevel(email_action_screen)
    comp_mail_screen.geometry("650x350")

    to = StringVar()
    sub = StringVar()
    body = StringVar()

    from_lable = Label(comp_mail_screen, text="From: ")
    from_lable.pack()
    from_entry = Entry(comp_mail_screen, textvariable=email, state='disabled', width=40)
    from_entry.pack()

    to_lable = Label(comp_mail_screen, text="To: ")
    to_lable.pack()
    to_entry = Entry(comp_mail_screen, textvariable=to, width=40)
    to_entry.pack()

    sub_lable = Label(comp_mail_screen, text="Subject: ")
    sub_lable.pack()
    sub_entry = Entry(comp_mail_screen, textvariable=sub, width=40)
    sub_entry.pack()

    body_lable = Label(comp_mail_screen, text="Body: ")
    body_lable.pack()
    body = ScrolledText(comp_mail_screen, wrap=WORD, width=70, height=10)
    body.pack()

    Button(comp_mail_screen, text="Send Mail", height="2", fg="green", width="30", command=send_mail).pack()


def email_action():
    global email_action_screen
    email_action_screen = Toplevel(main_screen)
    email_action_screen.title("Neutronmail - Email Actions")
    email_action_screen.geometry("300x300")

    Button(email_action_screen, text="Compose Mail", height="2", width="30", command=comp_mail).pack()
    Label(email_action_screen, text="").pack()

    Button(email_action_screen, text="View Mail", height="2", width="30", command=view_mail).pack()
    Label(email_action_screen, text="").pack()

    Button(email_action_screen, text="Exit", height="2", width="30", command=quit).pack()


def auth_check():
    global e_verify
    global pw_verify
    c = index_gui.signin(e_verify.get(), pw_verify.get())

    if(c == 2):
        Label(sign_in_screen, text="Invalid Email/Password", fg="red", font=("calibri", 15)).pack()
        sign_in_screen.after(1500, sign_in_screen.destroy())
        sign_in()
    else:
        sign_in_screen.after(1500, sign_in_screen.destroy())
        del pw_verify
        email_action()


def sign_in():
    global sign_in_screen
    sign_in_screen = Toplevel(main_screen)
    sign_in_screen.title("Neutronmail - Sign in")
    sign_in_screen.geometry("500x300")
    Label(sign_in_screen, text="Please enter details below to Sign in:").pack()
    Label(sign_in_screen, text="").pack()

    global e_verify
    global pw_verify

    e_verify = StringVar()
    pw_verify = StringVar()

    Label(sign_in_screen, text="Email: ").pack()
    email_sign_in_entry = Entry(sign_in_screen, textvariable=e_verify, width=40)
    email_sign_in_entry.pack()
    Label(sign_in_screen, text="").pack()
    Label(sign_in_screen, text="Password: ").pack()
    password_sign_in_entry = Entry(sign_in_screen, textvariable=pw_verify, show='*', width=40)
    password_sign_in_entry.pack()
    Label(sign_in_screen, text="").pack()

    Button(sign_in_screen, text="Sign In", width=10, height=1, command=auth_check).pack()


def register_user():
    global name
    global email
    global password

    ab = Label(sign_up_screen, text="Processing", fg="orange", font=("calibri", 10))
    ab.pack()

    r = index_gui.signup_helper(name.get(), email.get(), password.get())

    while True:
        if (r == 2):
            update_email_screen = Toplevel(main_screen)
            update_email_screen.title("Neutronmail - Update Email")
            update_email_screen.geometry("300x300")
            error_lable = Label(update_email_screen, text="Username is already taken", fg="red", font=("calibri", 15))
            error_lable.pack()
            email_lable = Label(update_email_screen, text="Username for email:* ")
            email_lable.pack()
            email_entry = Entry(update_email_screen)
            email_entry.pack()
            r = index_gui.signup_helper(name.get(), email_entry.get(), password.get())
            update_email_screen.destroy()
            del email_entry
        else:
            del name
            del email
            del password
            break

    ab.pack_forget()
    sign_up_screen.after(1000, Label(main_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack())
    sign_up_screen.destroy()

def sign_up():
    global name
    global password
    global email
    global sign_up_screen
    sign_up_screen = Toplevel(main_screen)
    sign_up_screen.title("Neutronmail - Sign Up")
    sign_up_screen.geometry("500x300")

    # Set text variables
    name = StringVar()
    password = StringVar()
    email = StringVar()

    # Set label for user's instruction
    Label(sign_up_screen, text="Please enter details below", bg="blue").pack()
    Label(sign_up_screen, text="").pack()

    # Set name label
    name_lable = Label(sign_up_screen, text="Name: ")
    name_lable.pack()

    # Set username entry
    # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.

    name_entry = Entry(sign_up_screen, textvariable=name, width=40)
    name_entry.pack()
    name_entry.focus_set()

    email_lable = Label(sign_up_screen, text="Username for email: ")
    email_lable.pack()

    email_entry = Entry(sign_up_screen, textvariable=email, width=40)
    email_entry.pack()

    # Set password label
    password_lable = Label(sign_up_screen, text="Password: ")
    password_lable.pack()

    # Set password entry
    password_entry = Entry(sign_up_screen, textvariable=password, show='*', width=40)
    password_entry.pack()

    Label(sign_up_screen, text="").pack()

    # Set register button
    Button(sign_up_screen, text="Register", width=10, height=1, bg="blue", command=register_user).pack()


def main_account_screen():
    global main_screen

    main_screen = Tk()
    main_screen.geometry("500x250")
    main_screen.title("Neutronmail")

    Label(text="Welcome to Neutronmail", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()

    Button(text="Sign In", height="2", width="30", command=sign_in).pack()
    Label(text="").pack()

    Button(text="Sign Up", height="2", width="30", command=sign_up).pack()

    main_screen.mainloop()


main_account_screen()
