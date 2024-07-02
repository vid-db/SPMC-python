from tkinter import *
from tkinter import ttk

from tkinter import messagebox
import mysql.connector

# Set up the MySQL connection
conn = mysql.connector.connect(host="localhost", user="root", password="", database="spmc")
mycursor = conn.cursor()

def product():
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = (screen_width - width) // 2
        y_coordinate = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')
        window.focus_set()  # Set focus to the window

    def display_and_update_table(tbl, cursor):
        sql = "SELECT * FROM product"
        cursor.execute(sql)

        for row in tbl.get_children():
            tbl.delete(row)

        i = 0
        for row in cursor:
            tbl.insert('', i, text="", values=(row[0], row[1], row[2], row[3], row[4]))
            i += 1

    def add(entrycode, entryname, entrybrand, entryprice, entryqty, tbl, mycursor):
        getprod_code = entrycode.get()
        getprod_name = entryname.get()
        getbrand = entrybrand.get()
        getprice = entryprice.get()
        getentryqty = entryqty.get()

        if not all([getprod_code, getprod_name, getbrand, getprice, getentryqty]):
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        if not (getprice.replace('.', '', 1).isdigit() and getentryqty.isdigit()):
            messagebox.showerror("Error", "Price and Quantity must be numeric.")
            return

        # Check if the product code already exists
        check_sql = "SELECT * FROM product WHERE product_code = %s"
        check_val = getprod_code,
        mycursor.execute(check_sql, check_val)
        existing_product = mycursor.fetchone()

        if existing_product:
            messagebox.showerror("Error", "Product code already exists.")
            return

        # Insert the new product
        insert_sql = "INSERT INTO product (product_code, product_name, brand, price, quantity) VALUES (%s, %s, %s, %s, %s)"
        insert_val = (getprod_code, getprod_name, getbrand, getprice, getentryqty)
        mycursor.execute(insert_sql, insert_val)
        conn.commit()
        messagebox.showinfo("Information", "Product inserted successfully.")

        # After adding the product, fetch and update the table
        display_and_update_table(tbl, mycursor)

        # Clear entry fields
        entrycode.delete(0, END)
        entryname.delete(0, END)
        entrybrand.delete(0, END)
        entryprice.delete(0, END)
        entryqty.delete(0, END)

    def update(tbl, entrycode, entryname, entrybrand, entryprice, entryqty, mycursor):
        selected_item = tbl.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a product to update.")
            return

        # Get the selected product code
        product_code = tbl.item(selected_item, "values")[0]

        # Retrieve updated data from entry widgets
        updated_name = entryname.get()
        updated_brand = entrybrand.get()
        updated_price = entryprice.get()
        updated_qty = entryqty.get()

        # Validate input
        if not all([updated_name, updated_brand, updated_price, updated_qty]):
            messagebox.showerror("Error", "Please select product to be updated.")
            return

        if not (updated_price.replace('.', '', 1).isdigit() and updated_qty.isdigit()):
            messagebox.showerror("Error", "Price and Quantity must be numeric.")
            return

        # Update the product in the database
        update_sql = "UPDATE product SET product_name = %s, brand = %s, price = %s, quantity = %s WHERE product_code = %s"
        update_val = (updated_name, updated_brand, updated_price, updated_qty, product_code)
        mycursor.execute(update_sql, update_val)
        conn.commit()

        # Update the product in the table
        tbl.item(selected_item, values=(product_code, updated_name, updated_brand, updated_price, updated_qty))

        messagebox.showinfo("Information", "Product updated successfully.")
        # Clear entry fields
        entrycode.delete(0, END)
        entryname.delete(0, END)
        entrybrand.delete(0, END)
        entryprice.delete(0, END)
        entryqty.delete(0, END)

    def display_selected(tbl, entrycode, entryname, entrybrand, entryprice, entryqty):
        selected_item = tbl.selection()

        if not selected_item:
            return

        # Get the data of the selected product
        product_data = tbl.item(selected_item, "values")

        # Display the data in the entry widgets
        entrycode.delete(0, END)
        entrycode.insert(0, product_data[0])

        entryname.delete(0, END)
        entryname.insert(0, product_data[1])

        entrybrand.delete(0, END)
        entrybrand.insert(0, product_data[2])

        entryprice.delete(0, END)
        entryprice.insert(0, product_data[3])

        entryqty.delete(0, END)
        entryqty.insert(0, product_data[4])

    def delete(tbl, mycursor):
        selected_item = tbl.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        # Get the selected product code
        product_code = tbl.item(selected_item, "values")[0]

        # Confirmation dialog before deleting
        confirm = messagebox.askyesno("Confirm Deletion", f"Do you want to delete the product with code {product_code}?")
        if not confirm:
            return

        # Delete the selected product from the database
        delete_sql = "DELETE FROM product WHERE product_code = %s"
        delete_val = (product_code,)
        mycursor.execute(delete_sql, delete_val)
        conn.commit()

        # Delete the selected product from the table
        tbl.delete(selected_item)

        messagebox.showinfo("Information", "Product deleted successfully.")

    def open_product_window():
        window = Tk()
        window.title("Product Inventory")
        window_width = 790
        window_height = 720
        center_window(window, window_width, window_height)
        window.resizable(False, False)
        window.tk_setPalette('#22092C')
        tbl = ttk.Treeview(window)
        # Bind the double click event to a function
        tbl.bind("<Double-1>", lambda event: display_selected(tbl, entrycode, entryname, entrybrand, entryprice, entryqty))
        titlelabel = Label(window, text="SAPANG PALAY TRANSPORT COOPERATIVE", font=('Poppins', 25), bd=2)
        titlelabel.grid(row=0, column=0, columnspan=8, padx=20, pady=20)

        prodcode = Label(window, text="Product Code", font=('Poppins', 15))
        prodname = Label(window, text="Product Name", font=('Poppins', 15))
        brand = Label(window, text="Brand", font=('Poppins', 15))
        prodprice = Label(window, text="Price", font=('Poppins', 15))
        prodqty = Label(window, text="Quantity", font=('Poppins', 15))
        prodcode.grid(row=1, column=0, padx=10, pady=10)
        prodname.grid(row=2, column=0, padx=10, pady=10)
        brand.grid(row=3, column=0, padx=10, pady=10)
        prodprice.grid(row=4, column=0, padx=10, pady=10)
        prodqty.grid(row=5, column=0, padx=10, pady=10)

        entrycode = Entry(window, width=43, bd=2, font=('Poppins', 15), bg='#ebdef6', fg='black')
        entryname = Entry(window, width=43, bd=2, font=('Poppins', 15), bg='#ebdef6', fg='black')
        entrybrand = Entry(window, width=43, bd=2, font=('Poppins', 15), bg='#ebdef6', fg='black')
        entryprice = Entry(window, width=43, bd=2, font=('Poppins', 15), bg='#ebdef6', fg='black')
        entryqty = Entry(window, width=43, bd=2, font=('Poppins', 15), bg='#ebdef6', fg='black')

        entrycode.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        entryname.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        entrybrand.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
        entryprice.grid(row=4, column=1, columnspan=3, padx=5, pady=5)
        entryqty.grid(row=5, column=1, columnspan=3, padx=5, pady=5)

        buttonadd = Button(
            window, text="Add", command=lambda: add(entrycode, entryname, entrybrand, entryprice, entryqty, tbl, mycursor),
            padx=5, pady=5, width=10, bd=3, font=('Poppins', 10), bg="#27ae60", fg='black'
        )
        buttonadd.grid(row=6, column=1, columnspan=1, padx=(5, 0), pady=(20, 0))

        buttonupdate = Button(
            window, text="Update", command=lambda: update(tbl, entrycode, entryname, entrybrand, entryprice, entryqty, mycursor), padx=5, pady=5, width=10, bd=3, font=('Poppins', 10), bg="#e3eb15", fg='black'
        )
        buttonupdate.grid(row=6, column=2, columnspan=1, pady=(20, 0))

        buttondelete = Button(
            window, text="Delete", command=lambda: delete(tbl, mycursor), padx=5, pady=5, width=10, bd=3, font=('Poppins', 10), bg="#BE3144", fg='black'
        )
        buttondelete.grid(row=6, column=3, columnspan=1, pady=(20, 0))

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Poppins', 15))

        tbl['columns'] = ("Code", "Product Name", "Brand", "Price", "Quantity")
        tbl.column("#0", width=0, stretch=NO)
        tbl.column("Code", anchor=CENTER, width=100)
        tbl.column("Product Name", anchor=W, width=150)
        tbl.column("Brand", anchor=W, width=100)
        tbl.column("Price", anchor=CENTER, width=100)
        tbl.column("Quantity", anchor=CENTER, width=100)

        tbl.heading("Code", text="Code", anchor=CENTER)
        tbl.heading("Product Name", text="Product Name", anchor=W)
        tbl.heading("Brand", text="Brand", anchor=W)
        tbl.heading("Price", text="Price", anchor=CENTER)
        tbl.heading("Quantity", text="Quantity", anchor=CENTER)
        tbl.grid(row=7, column=0, columnspan=8, rowspan=6, padx=40, pady=20)

        # Fetch and display initial data
        display_and_update_table(tbl, mycursor)

        window.mainloop()

    open_product_window()

    # Close the MySQL connection after the main loop
    conn.close()
