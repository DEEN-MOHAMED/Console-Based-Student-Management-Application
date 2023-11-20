from os import system
import mysql.connector
from typing import Callable
from os import name as osname
from .bl import check_input_type


if osname == 'posix':
    clear_command = 'clear'
else:
    clear_command = 'cls'


def create_record(student_info: dict, db):

        sql = """INSERT INTO Students (
        ID, Name, Age, Class,
        BirthDate, Gender, English, Language,
        Science, Social, Maths
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = [
            (
            student_info['student_number'],
            student_info['Name'],
            student_info['Age'],
            student_info['Class'],
            student_info['birth_date'],
            student_info['gender'],
            student_info['English'],
            student_info['Language'],
            student_info['Science'],
            student_info['Maths'],
            student_info['Social'],
            )
        ]

        result = check_input_type(student_detail=student_info)
        
        if result[0] == 'SUCCESS':
            
            cursor = db.cursor()

            try:
                cursor.executemany(sql, val)
                db.commit()
                return True, 'Done'

                
            except mysql.connector.Error as err:
                return err, False
            
        elif result[0] == 'FAILED':
            return '\n'.join(result[1]), 'FAILED'

        
def read_record(db, query: str = None) -> Callable:
        
        if query:
            sql = query

        else:
            sql = "SELECT * FROM Students;"
        
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            students = cursor.fetchall()
            return students
        
        except mysql.connector.Error as err:
            return f'Something went Wrong!{err}\n'


def update_record(column_name: str, new_value: str, id_: int, db) -> str:

    sql = f'UPDATE Students SET {column_name} = %s WHERE ID = %s'
    values = (new_value, id_)
    cursor = db.cursor()

    try:
        cursor.execute(sql, values)
        db.commit()
        system(clear_command)
        return 'Record Updated Succesfully.\n'
    
    except mysql.connector.Error as err:
        return f'Something went Wrong!{err}\n'


def delete_record(id_: int, db) -> str:

    cursor = db.cursor()
    sql = 'SELECT ID FROM Students WHERE ID=%s'
    value = (id_, )

    try:
        cursor.execute(sql, value)
        result = cursor.fetchone()
        if result:
            sql = 'DELETE FROM Students WHERE ID=%s'
            cursor.execute(sql, value)
            db.commit()
            return 'Student Deleted Succesfully.\n'
        else:
            return 'No Student Found!\n'
    
    except mysql.connector.Error as err:
        return f'Something went Wrong!{err}\n'