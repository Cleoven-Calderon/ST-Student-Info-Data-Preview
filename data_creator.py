import sqlite3
import qrcode
import os


DATA_BASE_NAME = "sample-database.db"


class StudentInfo:  # Main class
    all_students = []

    def __init__(self, db_name=DATA_BASE_NAME):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS students (
                        First_Name text,
                        Middle_Initial text,
                        Last_Name text,
                        ID integer,
                        QR_Path text
                        )""")
        self.conn.commit()

    def add_student(self, first_name: str, middle_init: str, last_name: str, stud_id: str, qrcode_path: str):
        students_format = {
            'First_Name': first_name,
            'Middle_Initial': middle_init,
            'Last_Name': last_name,
            'ID': stud_id,
            'QR_Path': qrcode_path
        }

        self.c.execute("INSERT INTO students VALUES (:First_Name, :Middle_Initial, :Last_Name, :ID, :QR_Path)",
                       students_format)
        self.conn.commit()
        return students_format

    def get_all_students(self):
        self.c.execute("SELECT * FROM students")
        return self.c.fetchall()

    def close(self):
        self.conn.close()


def get_valid_name(prompt, allow_single=False):
    """Ensures that the input only contains letters and spaces.
       If allow_single=True, ensures it's exactly one letter (for middle initial)."""
    while True:
        name = input(prompt).strip()
        if not all(ch.isalpha() or ch.isspace() for ch in name):
            print("❌ Only letters and spaces are allowed. Please try again.")
            continue
        if allow_single and len(name) != 1:
            print("❌ Middle initial must be exactly one letter.")
            continue
        if not name:
            print("❌ Field cannot be empty.")
            continue
        return name


# Usage
if __name__ == "__main__":
    while True:
        try:
            db = StudentInfo()

            qr_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qrcodes")
            os.makedirs(qr_dir, exist_ok=True)

            # Validated inputs
            f_name = get_valid_name("Enter first name: ").title()
            m_name = get_valid_name("Enter middle initial: ", allow_single=True).upper()
            l_name = get_valid_name("Enter last name: ").capitalize()
            student_id = input("Enter student ID: ").strip()

            print("QR code created!")

            qr_name = f"{f_name} {m_name} {l_name}.png"
            qr_data = f"{student_id}"

            img = qrcode.make(qr_data)
            filepath = os.path.join(qr_dir, qr_name)
            img.save(filepath)

            db.add_student(f_name, m_name + '.', l_name, student_id, filepath)
            db.close()

            print(f"✅ Student {f_name} {m_name}. {l_name} added successfully!\n")
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")
