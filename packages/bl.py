def check_input_type(student_detail: dict):

    err_list = list()

    for key, value in student_detail.items():
        if value:
            if key in ['Social_score', 'Language_score', 'English_score', 'Science_score', 'Maths_score'] and type(value) != str:
                err_list.append(f'- {key} must be float/integer!')
        elif not value:
            err_list.append(f'- {key} field is empty!')
        else:
            continue

    if err_list:
        return 'FAILED', err_list
    
    return 'SUCCESS', err_list