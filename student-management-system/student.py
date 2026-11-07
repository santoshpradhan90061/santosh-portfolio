import csv
import sqlite3

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    marks REAL NOT NULL
)
""")

conn.commit()


# Add Student
def add_student():
    name = input("Enter student name: ")
    roll_no = int(input("Enter roll number: "))
    marks = float(input("Enter student marks: "))

    try:
        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?)",
            (roll_no, name, marks)
        )
        conn.commit()
        print("Student added successfully!")

    except sqlite3.IntegrityError:
        print("Roll number already exists!")


# View Students
def view_students():
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if records:
        print("\nStudent Records:")
        for student in records:
            print("--------------------")
            print("Roll Number:", student[0])
            print("Name:", student[1])
            print("Marks:", student[2])
    else:
        print("No student records found.")


# Delete Student
def delete_student():
    roll_no = int(input("Enter roll number to delete: "))

    cursor.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )
    conn.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student not found.")


# Search Student
def search_student():
    roll_no = int(input("Enter roll number to search: "))

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    if student:
        print("\nStudent Found!")
        print("Roll Number:", student[0])
        print("Name:", student[1])
        print("Marks:", student[2])
    else:
        print("Student not found.")
def update_student():
    roll_no = int(input("Enter roll number to update: "))

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    if student:
        name = input("Enter new name: ")
        marks = float(input("Enter new marks: "))

        cursor.execute(
            "UPDATE students SET name = ?, marks = ? WHERE roll_no = ?",
            (name, marks, roll_no)
        )

        conn.commit()
        print("Student updated successfully!")
    else:
        print("Student not found.")

def calculate_grade():
    roll_no = int(input("Enter roll number: "))

    cursor.execute(
        "SELECT name, marks FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    if student:
        name, marks = student

        if marks >= 90:
            grade = "A"
        elif marks >= 80:
            grade = "B"
        elif marks >= 70:
            grade = "C"
        elif marks >= 60:
            grade = "D"
        else:
            grade = "F"

        print("\nStudent Name:", name)
        print("Marks:", marks)
        print("Grade:", grade)

    else:
        print("Student not found.")

    import csv

def export_students():
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if records:
        with open("students.csv", "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["Roll Number", "Name", "Marks"])
            writer.writerows(records)

        print("Student records exported successfully!")
        print("File saved as students.csv")
    else:
        print("No student records to export.")

def import_students():
    try:
        with open("students.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            imported = 0
            skipped = 0

            for row in reader:
                try:
                    roll_no = int(row["Roll Number"])
                    name = row["Name"]
                    marks = float(row["Marks"])

                    cursor.execute(
                        "INSERT OR IGNORE INTO students VALUES (?, ?, ?)",
                        (roll_no, name, marks)
                    )

                    if cursor.rowcount > 0:
                        imported += 1
                    else:
                        skipped += 1

                except (ValueError, KeyError):
                    skipped += 1

            conn.commit()

            print("Import completed successfully!")
            print("Records imported:", imported)
            print("Records skipped:", skipped)

    except FileNotFoundError:
        print("students.csv file not found!")


def class_summary():
    cursor.execute("""
        SELECT AVG(marks), MAX(marks)
        FROM students
    """)

    result = cursor.fetchone()
    average, highest = result

    if average is not None:
        print("\n===== Class Summary =====")
        print("Class Average:", round(average, 2))
        print("Highest Marks:", highest)

        cursor.execute("""
            SELECT roll_no, name, marks
            FROM students
            WHERE marks = ?
        """, (highest,))

        toppers = cursor.fetchall()

        print("\nHighest Scoring Student(s):")

        for student in toppers:
            print("Roll Number:", student[0])
            print("Name:", student[1])
            print("Marks:", student[2])
    else:
        print("No student records found.")

# Main Menu
while True:
    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Delete Student")
    print("4. Search Student")
    print("5. Update Student")
    print("6. Calculate Grade")
    print("7. Export Student Record")
    print("8. Import Student Record")
    print("9. Class Summary")
    print("10. Exit")


    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        delete_student()

    elif choice == "4":
        search_student()

    elif choice == "5":
        update_student()

    elif choice == "6":
        calculate_grade()
        
    elif choice == "7":
        export_students()

    elif choice == "8": 
        import_students()

    elif choice == "9": 
        class_summary()

    elif choice == "10":       
        print("Thank You!")
        break

    else:
        print("Invalid choice. Try again.")

# Close database connection
conn.close()