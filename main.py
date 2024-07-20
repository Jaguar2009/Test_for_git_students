import sqlite3


def create_database():
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            major TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            instructor TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students_courses (
            student_id INTEGER,
            course_id INTEGER,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (course_id)
        )
    ''')

    conn.commit()
    conn.close()


def add_student(name, age, major):
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, major) VALUES (?, ?, ?)', (name, age, major))
    conn.commit()
    conn.close()


def add_course(course_name, instructor):
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO courses (course_name, instructor) VALUES (?, ?)', (course_name, instructor))
    conn.commit()
    conn.close()


def show_students():
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    for student in students:
        print(student)


def show_courses():
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()
    for course in courses:
        print(course)


def register_student_to_course(student_id, course_id):
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students_courses (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
    conn.commit()
    conn.close()


def show_students_for_course(course_id):
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.name, s.age, s.major
        FROM students s
        JOIN students_courses sc ON s.id = sc.student_id
        WHERE sc.course_id = ?
    ''', (course_id,))
    students = cursor.fetchall()
    conn.close()
    for student in students:
        print(student)


def get_input(prompt, cast_type=str):
    while True:
        value = input(prompt).strip()
        if value:
            try:
                return cast_type(value)
            except ValueError:
                print(f"Некоректний ввід. Будь ласка, введіть значення типу {cast_type.__name__}.")
        else:
            print("Поле не може бути пустим. Будь ласка, введіть значення.")


def main():
    create_database()

    while True:
        print("\n1. Додати нового студента")
        print("2. Додати новий курс")
        print("3. Показати список студентів")
        print("4. Показати список курсів")
        print("5. Зареєструвати студента на курс")
        print("6. Показати студентів на конкретному курсі")
        print("7. Вийти")

        choice = get_input("Оберіть опцію (1-7): ", int)

        if choice == 1:
            name = get_input("Введіть ім'я студента: ")
            age = get_input("Введіть вік студента: ", int)
            major = get_input("Введіть спеціальність студента: ")
            add_student(name, age, major)

        elif choice == 2:
            course_name = get_input("Введіть назву курсу: ")
            instructor = get_input("Введіть викладача курсу: ")
            add_course(course_name, instructor)

        elif choice == 3:
            show_students()

        elif choice == 4:
            show_courses()

        elif choice == 5:
            student_id = get_input("Введіть ID студента: ", int)
            course_id = get_input("Введіть ID курсу: ", int)
            register_student_to_course(student_id, course_id)

        elif choice == 6:
            course_id = get_input("Введіть ID курсу: ", int)
            show_students_for_course(course_id)

        elif choice == 7:
            break

        else:
            print("Некоректний вибір. Будь ласка, введіть число від 1 до 7.")


if __name__ == "__main__":
    main()
