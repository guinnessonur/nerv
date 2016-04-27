from Tkinter import *
import mysql.connector


class GUI:
    def __init__(self):

        self.cnx = mysql.connector.connect(user="root", password="root", host="127.0.0.1", database="nerv")
        self.cursor = self.cnx.cursor()

        self.log_array = []

        # Window creation
        self.window = Tk()
        self.window.title("Nerv GUI 1.0")
        self.window.geometry("800x600+100+100")
        self.window.resizable(width=FALSE, height=FALSE)

        #Menu bar
        self.menubar = Menu(self.window)

        # --------- #
        # File Menu #
        # --------- #

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Add New Book", command=self.add_new_book)
        self.filemenu.add_command(label="Add New Media", command=self.add_new_media)
        self.filemenu.add_command(label="Add New Customer", command=self.add_new_customer)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Preferences", command=self.preferences)
        self.filemenu.add_command(label="Exit", command=self.menu_exit)

        self.menubar.add_cascade(label="File", menu=self.filemenu)


        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Edit Book")
        self.editmenu.add_command(label="Edit Media")
        self.editmenu.add_command(label="Edit Customer")
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.menubar.add_command(label="About", command=self.menu_about)
        self.menubar.add_command(label="Help")

        self.menubar.add_separator()
        self.window.config(menu=self.menubar)

        # ----------- #
        # Top Screen  #
        # ----------- #

        self.barcode_label = Label(text="Barcode:")
        self.barcode_label.place(x=15, y=17)

        self.barcode_input = Entry()
        self.barcode_input.place(x=75, y=15, height=25)

        self.add_to_cart = Button(text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart.place(x=210, y=15, width=75)

        self.empty_cart = Button(text="Discard Cart", command=self.empty_cart)
        self.empty_cart.place(x=290, y=15, width=75)

        self.cart = Listbox()
        self.cart.place(x=15, y=50, height=115, width=350)

        self.label_separator = Label(relief=SUNKEN)
        self.label_separator.place(x=380, y=0, height=175, width=2)

        self.customer_label = Label(text="ID or Name: ")
        self.customer_label.place(x=390, y=15)

        self.customer_input = Entry()
        self.customer_input.place(x=500, y=15)

        self.phone_label = Label(text="Phone Number: ")
        self.phone_label.place(x=390, y=45)

        self.phone_input = Entry()
        self.phone_input.place(x=500, y=45)

        self.payment_label = Label(text="Payment Method: ")
        self.payment_label.place(x=390, y=80)

        self.payment_method = StringVar(self.window)
        self.payment_method.set("Cash")
        self.payment_option = OptionMenu(self.window, self.payment_method, "Cash", "Credit Card")
        self.payment_option.place(x=500, y=75, width=125)

        self.check_out_button = Button(text="Checkout", command=self.check_out)
        self.check_out_button.place(x=390, y=115, height=50, width=110)

        self.cancel_order_button = Button(text="Cancel", command=self.cancel_order)
        self.cancel_order_button.place(x=515, y=115, height=50, width=110)

        self.logo_separator = Label(relief=SUNKEN)
        self.logo_separator.place(x=635, y=0, height=175, width=2)

        photo = PhotoImage(file="NervLogo.gif")
        logo_label = Label(image=photo)
        logo_label.image = photo
        logo_label.place(x=650, y=10)

        # ------------- #
        # Bottom Screen #
        # ------------- #

        separator = Frame(height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=175)

        self.log_label = Label(text="Log:")
        self.log_label.place(x=15, y=190)

        self.log_input = Entry()
        self.log_input.place(x=65, y=190, width=550)

        self.search_label = Label(text="Search:")
        self.search_label.place(x=15, y=215, height=20)

        self.search_input = Entry()
        self.search_input.place(x=65, y=215, width=550)

        self.search_button = Button(text="Search", command=self.search)
        self.search_button.place(x=625, y=190, width=75, height=45)

        self.reset_button = Button(text="Reset", command=self.reset)
        self.reset_button.place(x=710, y=190, width=75, height=45)

        self.listbox = Listbox(self.window)
        self.listbox.place(x=15, y=245, width=770, height=340)

        self.window.mainloop()

    def check_out(self):
        the_cart = self.cart.get(0, END)
        for i in the_cart:
            i = self.customer_input.get() + ", " + i + ", " + self.payment_method.get()
            self.log_array.append(i)
        self.cancel_order()

        successful = Toplevel(self.window)
        successful.title("Checkout Successful!")
        successful.geometry("150x75")

        successful_label = Label(successful, text="Checkout Successful!")
        successful_label.place(x=15, y=15)
        thank_you = Label(successful, text="Thank you! :-)")
        thank_you.place(x=35, y=35)

    def cancel_order(self):
        self.barcode_input.delete(0, END)
        self.cart.delete(0, END)
        self.customer_input.delete(0, END)
        self.phone_input.delete(0, END)

    def add_to_cart(self):
        barcode = self.barcode_input.get()

        self.cursor.execute("SELECT * FROM Books WHERE Barcode={}".format(barcode))
        row = self.cursor.fetchall()
        for every_element in row:
            element = ', '.join(str(i) for i in every_element)
            self.cart.insert(END, element)

        self.cursor.execute("SELECT * FROM Media WHERE Barcode={}".format(barcode))
        row = self.cursor.fetchall()
        for every_element in row:
            element = ', '.join(str(i) for i in every_element)
            self.cart.insert(END, element)

    def empty_cart(self):
        self.cart.delete(0, END)
        self.barcode_input.delete(0, END)

    def change_label(self):
        self.label_title = self.inputs.get()
        self.label["text"] = self.label_title

    def search(self):
        self.listbox.delete(0, END)

        log_in = self.log_input.get()
        if log_in != "":
            for i in self.log_array:
                self.listbox.insert(END, i)
            return

        search_in = self.search_input.get()
        if search_in != "":
            try:
                self.cursor.execute("SELECT * FROM Books WHERE {};".format(search_in))
                rows = self.cursor.fetchall()
                for every_element in rows:
                    element = ', '.join(str(i) for i in every_element)
                    element = "Book: " + element
                    self.listbox.insert(END, element)
            except Exception:
                pass
            try:
                self.cursor.execute("SELECT * FROM Media WHERE {};".format(search_in))
                rows = self.cursor.fetchall()
                for every_element in rows:
                    element = ', '.join(str(i) for i in every_element)
                    element = "Media: " + element
                    self.listbox.insert(END, element)
                return
            except Exception:
                pass

    def reset(self):
        self.listbox.delete(0, END)
        self.log_input.delete(0, END)
        self.search_input.delete(0, END)

    def add_new_book(self):
        #Add New Book
        item_window = Toplevel(self.window)
        item_window.title("Add New Book")
        item_window.geometry("275x275")
        item_window.resizable(width=FALSE, height=FALSE)
        #Book Title
        title_label = Label(item_window, text="Book Title")
        title_label.place(x=25, y=15)
        input_title = Entry(item_window)
        input_title.place(x=115, y=15)
        #Author
        aut_label = Label(item_window, text="Author")
        aut_label.place(x=25, y=45)
        input_aut = Entry(item_window)
        input_aut.place(x=115, y=45)
        #Publisher
        pub_label = Label(item_window, text="Publisher")
        pub_label.place(x=25, y=75)
        input_pub = Entry(item_window)
        input_pub.place(x=115, y=75)
        #ISBN
        isbn_label = Label(item_window, text="ISBN")
        isbn_label.place(x=25, y=105)
        input_isbn= Entry(item_window)
        input_isbn.place(x=115, y=105)
        #Price
        price_label = Label(item_window, text="Price")
        price_label.place(x=25, y=135)
        input_price= Entry(item_window)
        input_price.place(x=115, y=135)
        #Genre
        genre_label = Label(item_window, text="Genre")
        genre_label.place(x=25, y=165)
        input_genre = Entry(item_window)
        input_genre.place(x=115, y=165)
        #Barcode
        brcd_label = Label(item_window, text="Barcode")
        brcd_label.place(x=25, y=195)
        input_brcd = Entry(item_window)
        input_brcd.place(x=115, y=195)

        #Add Book
        add_book = Button(item_window, text="Add Book!", command=lambda: self.send_book_query("\"{}\", \"{}\", \"{}\", \"{}\", {}, \"{}\", {}".format(input_title.get(), input_aut.get(), input_pub.get(), input_isbn.get(), input_price.get(), input_genre.get(), input_brcd.get())))
        add_book.place(x=100, y=230, width=150)

        #item_window.mainloop()

    def send_book_query(self, query_values):
        self.cursor.execute("INSERT INTO Books VALUES({})".format(query_values))
        self.cnx.commit()

    def add_new_media(self):
        item_window = Toplevel(self.window)
        item_window.title("Add New Media")
        item_window.geometry("275x215")
        item_window.resizable(width=FALSE, height=FALSE)

        # Media Title
        title_label = Label(item_window, text="Media Title")
        title_label.place(x=25, y=15)
        input_title = Entry(item_window)
        input_title.place(x=115, y=15)

        # Composer
        com_label = Label(item_window, text="Composer")
        com_label.place(x=25, y=45)
        input_com = Entry(item_window)
        input_com.place(x=115, y=45)

        # Price
        price_label = Label(item_window, text="Price")
        price_label.place(x=25, y=75)
        input_price = Entry(item_window)
        input_price.place(x=115, y=75)

        # Genre
        gen_label = Label(item_window, text="Genre")
        gen_label.place(x=25, y=105)
        input_gen = Entry(item_window)
        input_gen.place(x=115, y=105)

        # ISBN
        bar_label = Label(item_window, text="Barcode")
        bar_label.place(x=25, y=135)
        input_bar = Entry(item_window)
        input_bar.place(x=115, y=135)

        # Add Book
        add_book = Button(item_window, text="Add Media!", command=lambda: self.send_media_query("\"{}\", \"{}\", {}, \"{}\", {}".format(input_title.get(), input_com.get(), input_price.get(), input_gen.get(), input_bar.get())))
        add_book.place(x=100, y=170, width=150)

    def send_media_query(self, query_values):
        self.cursor.execute("INSERT INTO Media VALUES({})".format(query_values))
        self.cnx.commit()

    def add_new_customer(self):
        item_window = Toplevel(self.window)
        item_window.title("Add New Customer")
        item_window.geometry("275x150")
        item_window.resizable(width=FALSE, height=FALSE)

        #Customer Name
        name_label = Label(item_window, text="Name")
        name_label.place(x=25, y=15)
        input_name = Entry(item_window)
        input_name.place(x=115, y=15)

        #Address
        loc_label = Label(item_window, text="Address")
        loc_label.place(x=25, y=45)
        input_loc = Entry(item_window)
        input_loc.place(x=115, y=45)

        #Age
        age_label = Label(item_window, text="Age")
        age_label.place(x=25, y=75)
        input_age = Entry(item_window)
        input_age.place(x=115, y=75)

        #Add Customer
        add_customer = Button(item_window, text="Add Customer!", command=lambda: self.send_customer_query("\"{}\", \"{}\", \"{}\"".format(input_name.get(), input_loc.get(), input_age.get())))
        add_customer.place(x=100, y=110, width=150)

    def send_customer_query(self, query_values):
        self.cursor.execute("INSERT INTO Customers(name, location, AGE) VALUES({})".format(query_values))
        self.cnx.commit()

    def edit_book(self):
        return 0

    def edit_media(self):
        return 0

    def edit_customer(self):
        return 0

    def menu_exit(self):
        exit_window = Toplevel(self.window)
        exit_window.title("No way :-(")
        exit_window.geometry("150x80")
        exit_window.resizable(width=FALSE, height=FALSE)
        exit_label = Label(exit_window, text="Do you really want to exit?")
        exit_label.place(x=5, y=5)

        yes_button = Button(exit_window, text="Yes", command=self.window.quit)
        yes_button.place(x=25, y=35, width=35)
        no_button = Button(exit_window, text="No", command=exit_window.destroy)
        no_button.place(x=85, y=35, width=35)

    def preferences(self):
        pref_window = Toplevel(self.window)
        pref_window.title("Preferences")
        pref_window.geometry("200x300")

    def menu_about(self):
        about_window = Toplevel(self.window)
        about_window.title("About")
        #atago = PhotoImage(file="makiabout.gif")
        #about_photo = Label(about_window, image=atago)
        #about_photo.image = atago
        #about_photo.pack()
        about_window.resizable(width=FALSE, height=FALSE)

GUI()
