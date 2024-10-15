class Mentor:
    def __init__(self, name, surname, courses=[]):
        self.name = name
        self.surname = surname
        self.courses_attached = courses
class Lecturer(Mentor):
    def __init__(self, name, surname, courses=[]):
        super().__init__(name, surname, courses)
        self.grades = {}

    def __str__(self):
        avg_grade = self._average_grade()
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade:.2f}'
    
    # Средний балл
    def _average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    # Сравнение лекторов
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

class Reviewer(Mentor):
    def __init__(self, name, surname, courses=[]):
        super().__init__(name, surname, courses)
    
    # Выставление оценок 
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

class Student:
    def __init__(self, name, surname, courses_in_progress=[], finished_courses=[]):
        self.name = name
        self.surname = surname
        self.courses_in_progress = courses_in_progress
        self.finished_courses = finished_courses
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'
    def __str__(self):
        avg_grade = self._average_grade()
        return (f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {avg_grade:.2f}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')
    
    def _average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

def average_student_grade(students, course):
    total_grades = []
    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])
    if total_grades:
        return sum(total_grades) / len(total_grades)
    return 0

def average_lecturer_grade(lecturers, course):
    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades.extend(lecturer.grades[course])
    if total_grades:
        return sum(total_grades) / len(total_grades)
    return 0

student1 = Student('Ruoy', 'Eman', ['Python'], ['Введение в программирование'])
student2 = Student('John', 'Doe', ['Python'])

lecturer1 = Lecturer('Some', 'Buddy', ['Python'])
lecturer2 = Lecturer('Jane', 'Smith', ['Python'])

reviewer1 = Reviewer('Review', 'Master', ['Python'])
reviewer2 = Reviewer('Expert', 'Checker', ['Python'])

reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 8)

student1.rate_lecturer(lecturer1, 'Python', 10)
student2.rate_lecturer(lecturer1, 'Python', 9)

print(reviewer1)
print(lecturer1)
print(student1)

print(lecturer1 < lecturer2)
print(student1 < student2)

print('Средняя оценка студентов по Python:', average_student_grade([student1, student2], 'Python'))
print('Средняя оценка лекторов по Python:', average_lecturer_grade([lecturer1, lecturer2], 'Python'))
