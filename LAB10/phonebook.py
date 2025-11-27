import psycopg2
import csv

try:
    connection = psycopg2.connect(
        host = "127.0.0.1",
        user = "postgres",
        password = "madina2000000",
        dbname = "postgres"
    )
    cursor = connection.cursor()
    
    def console():
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        cursor.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
        connection.commit()
        print("Added successfully.\n")

    def from_csv():
        # C:\\Users\\Madina Zheleu\\OneDrive\\Рабочий стол\\contacts.csv
        file = input("Enter CSV file path: ")
        try:
            with open(file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    name, phone = row
                    cursor.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",(name, phone))
                connection.commit()
            print("CSV uploaded successfully.\n")
        except Exception as ex:
            print("CSV upload error:", ex, "\n")

    def update_user():
        phone = input("Enter phone number of contact to update: ")
        new_name = input("Enter new name (leave empty to skip): ")
        new_phone = input("Enter new phone (leave empty to skip): ")

        if new_name:
            cursor.execute("UPDATE phonebook SET name=%s WHERE phone=%s", (new_name, phone))
        if new_phone:
            cursor.execute("UPDATE phonebook SET phone=%s WHERE phone=%s", (new_phone, phone))
        connection.commit()
        print("Updated successfully.\n")

    def search():
        print("\nFilters:")
        print("1 — By name")
        print("2 — By phone")
        choice = input("Select: ")

        if choice == "1":
            name = input("Enter name: ")
            cursor.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (name,))
        elif choice == "2":
            phone = input("Enter phone: ")
            cursor.execute("SELECT * FROM phonebook WHERE phone=%s", (phone,))
        else:
            print("Wrong option.")
            return

        rows = cursor.fetchall()
        print("Results:")
        for row in rows:
            print(row)
        print()

    def delete_user():
        print("\nDelete by:")
        print("1 — name")
        print("2 — phone")
        choice = input("Select: ")

        if choice == "1":
            name = input("Enter name: ")
            cursor.execute("DELETE FROM phonebook WHERE name=%s", (name,))
        elif choice == "2":
            phone = input("Enter phone: ")
            cursor.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
        else:
            print("Wrong option.")
            return
        connection.commit()
        print("Deleted successfully.\n")

    while True:
        print("===== PHONEBOOK MENU =====")
        print("1 — Add from console")
        print("2 — Add from CSV")
        print("3 — Update")
        print("4 — Search")
        print("5 — Delete")
        print("6 — Show all")
        print("0 — Exit")

        choice = input("Select: ")

        if choice == "1":
            console()
        elif choice == "2":
            from_csv()
        elif choice == "3":
            update_user()
        elif choice == "4":
            search()
        elif choice == "5":
            delete_user()
        elif choice == "6":
            cursor.execute("SELECT * FROM phonebook ORDER BY id")
            for row in cursor.fetchall():
                print(row)
            print()
        elif choice == "0":
            break
        else:
            print("Invalid option.\n")

except Exception as ex:
    print("[INFO] Error🚨", ex)
    
finally:
    cursor.close()
    connection.close()
    print("Program finished.")
  
    

  