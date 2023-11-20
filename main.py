import os
from os import system
import mysql.connector
from typing import List
from typing import Callable
from os import name as osname
from tabulate import tabulate
import mysql.connector.errors
from package.dal import create_record, read_record, delete_record, update_record


if osname == 'posix':
    clear_command = 'clear'
else:
    clear_command = 'cls'

db = mysql.connector.connect(

    host="localhost",
    user="root",
    password="MYSQLdheen#7",
    database="student"
    )

class StudentManager:

    def __init__(self) -> None:
        pass
        

    def add_student(self):

        self.student_info = dict()

        self.Class = input('Student Class: ')
        self.student_number = input('Student Number: ')
        self.Name = input('Student Name: ')
        self.Age = input('Student Age: ')
        self.gender = input('Student Gender(M/F): ')
        self.birth_date = input('Student Birthdate (YYYY-MM-DD): ')
        self.Language = input('Student Language Score: ')
        self.English = input('Student English Score: ')
        self.Maths = input('Student Maths Score: ')
        self.Science = input('Student Science Score: ')
        self.Social = input('Student Social Score: ')

        self.student_info['Name'] = self.Name
        self.student_info['Age'] = self.Age
        self.student_info['gender'] = self.gender
        self.student_info['Class'] = self.Class
        self.student_info['student_number'] = self.student_number
        self.student_info['birth_date'] = self.birth_date
        self.student_info['Language'] = self.Language
        self.student_info['English'] = self.English
        self.student_info['Maths'] = self.Maths
        self.student_info['Science'] = self.Science
        self.student_info['Social'] = self.Social

        system(clear_command)

        result = create_record(self.student_info, db)
        if result[1] == 'Done':
        
            return f'{self.Name} Saved.\n'
        
        else:
            return f'Failed Because:\n{result[0]}\n'
    

    def show_student(self) -> Callable:

        system(clear_command)
        print('List of Students:')

        students = read_record(db)
        if students:
            return self.__printer(students)


    def __printer(self, value: List) -> str:

        title = ['ID', 'Name', 'Age', 'Class', 'Birth Date', 'Gender', 'English Score',  'Language Score', 'Science Score', 'Social Score', 'Maths Score']
        table = tabulate(value, headers=title, tablefmt='psql')

        return f'{table}\n'


    def edit_student(self, id_: int, edited_column: str) -> Callable:

        value_translate = {
            '1': 'Name',
            '2': 'Age',
            '3': 'ID',
            '4': 'Class',
            '5': 'Gender',
            '6': 'BirthDate',
            '7': 'English',
            '8': 'Maths',
            '9': 'Science',
            '10': 'Social',
            '11': 'Language'
        }

        if edited_column not in value_translate:
            system(clear_command)
            return 'You Must enter a Number Between 1-11!\n'
        
        value = value_translate[edited_column]
        system(clear_command)
        new_value = input(f'Enter New {value}: ')

        try:
            student_exists_query = f'SELECT ID from Students WHERE ID = {id_}'
            cursor = db.cursor()
            cursor.execute(student_exists_query)
            data = cursor.fetchone()

            if data:

                return update_record(value, new_value, id_, db)
            else:
                return 'No Students Found!\n'
            
        except mysql2.connector.Error as err:
            return f'SomeThing Went Wrong!, {err}'
    
            
    def remove_student(self, id_: int) -> Callable:

        system(clear_command)

        return delete_record(id_, db)


    def search_student(self, search_option: str, student_id: str) -> Callable:

        system(clear_command)

        value_translate = {
            '1': 'Name',
            '2': 'Age',
            '3': 'Gender',
            '4': 'Class',
            '5': 'ID'
            }
        
        if search_option not in value_translate:
            return 'You Must enter a Number Between 1-5!\n'
        
        value = value_translate[search_option]
        sql_query = f'SELECT * FROM Students WHERE {value} = "{student_id}"'

        result = read_record(db, sql_query)

        if result:
            return self.__printer(result)
    def class_average(self, student_class: str) -> Callable:

        system(clear_command)
        sql_query = f"""SELECT AVG((Language + English + Maths + Science + Social) / 5) AS AveragePercentage 
                        FROM Students 
                        WHERE Class = "{student_class}" """
        result = read_record(db, sql_query)

        if result:
            return f'Average Percentage for Class {student_class}: {result[0][0]:.2f}%\n'
        else:
            return f'No students found in Class {student_class}.\n'

    def student_average(self, student_id: int) -> Callable:
        
        system(clear_command)
        sql_query = f"""SELECT (Language + English + Maths + Science + Social) / 5 AS AverageMarks 
                        FROM Students 
                        WHERE ID = {student_id}"""

        result = read_record(db, sql_query)

        if result:
            return result[0][0]
        else:
            return -1

    def best_student(self, course: str) -> Callable:
        system(clear_command)
        value_translate = {
            '1': 'Language',
            '2': 'English',
            '3': 'Maths',
            '4': 'Science',
            '5': 'Social'
        }

        if course not in value_translate:
            return 'You Must enter a Number Between 1-5!\n'
        value = value_translate[course]
        sql_query = f"""SELECT MAX({value}) FROM Students"""
        result = read_record(db, sql_query)

        if result:
            return self.__printer(result)


if __name__ == '__main__':

    student_manager = StudentManager()
    while True:
        options = input('1-Add Student\n2-Show Student\n3-Edit Student\n4-Remove Student\n5-Search Student\n6-Find Best Student By Score\n7-Class Average\n8-Student Average and Grades\n9-Exit\n\nHow Can I Help You: ')
        system(clear_command)

        if options == '1':
            system(clear_command)
            print(student_manager.add_student())

        elif options == '2':
            print(student_manager.show_student())

        elif options == '3':
            system(clear_command)
            student_id = int(input('Student Number: '))
            print()
            student_exists_query = f'SELECT ID from Students WHERE ID = {student_id}'
            cursor = db.cursor()
            cursor.execute(student_exists_query)
            data = cursor.fetchone()
            
            if not data:
                system(clear_command)
                print('No Students Found!\n')
            else:
                system(clear_command)
                edited_attribute = input('What Do you Want to Update:\n\n1-Name\n2-Age\n3-Student Number\n4-Class\n5-Gender\n6-Birth Date\n7-English Score\n8-Maths Score\n9-Science Score\n10-Social Score\n11 Language Score\n\nWhich One: ')
                print(student_manager.edit_student(student_id, edited_attribute))

        elif options == '4':
            system(clear_command)
            student_id = int(input('Enter Student Number: '))
            print(student_manager.remove_student(student_id))

        elif options == '5':
            system(clear_command)
            while True:
                search_option = input('Search Student By:\n\n1-Name:\n2-Age\n3-Gender\n4-Class\n5-Student Number\n6-Exit\n\nWhich One: ') 
                if search_option == '6':
                    system(clear_command)
                    print('Exit')
                    print()
                    break

                value_translate = {
                    '1': 'Name',
                    '2': 'Age',
                    '3': 'Gender',
                    '4': 'Class',
                    '5': 'ID',
                    }
                
                if search_option not in value_translate:
                    system(clear_command)
                    print('You Have To Enter a Number Between 1-6!')
                    break

                student_id = input(f'Enter Student {value_translate[search_option]}:')
                print(f'++ Filter by {value_translate[search_option]} ++')
                print()
                print(student_manager.search_student(search_option, student_id))
                break

        elif options == '6':
            system(clear_command)
            while True:
                filter_by = input('Find Best Student By:\n\n1 Language Score\n2-English Score\n3-Maths Score\n4-Science Score\n5-Social Score\n\nWhich one: ')
                value_translate = {
                    '1': 'Language',
                    '2': 'English',
                    '3': 'Maths',
                    '4': 'Science',
                    '5': 'Social'
                }
                if filter_by not in value_translate:
                    system(clear_command)
                    print('You Have To Choose Between (1-5)!')
                    print()
                print(student_manager.best_student(filter_by))
                break

        elif options == '7':
            system(clear_command)
            student_class = input('Enter the class for which you want to calculate the average percentage: ')
            print(student_manager.class_average(student_class))

        elif options == '8':
            system(clear_command)
            student_id = int(input('Enter the ID of the student for which you want to calculate the average marks: '))
            stuavg=student_manager.student_average(student_id)
            print(student_manager.student_average(student_id))
            if(stuavg >= 90):
                print("Your Grade is : A+")
            elif(stuavg >= 80 and stuavg <= 89):
                print("Your Grade is : A")    
            elif(stuavg >= 70 and stuavg <= 79):
                print("Your Grade is : B")
            elif(stuavg >= 60 and stuavg <= 69):
                print("Your Grade is : C")
            elif(stuavg >= 50 and stuavg <=59):
                print("Your Grade is : D")
            elif(stuavg < 50 and stuavg>=0):
                print("Your Grade is : F")
            else:
                print("No student found for this id")                       
        elif options == '9':
            system(clear_command)
            print('Good Bye.')
            break