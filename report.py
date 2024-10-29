import psycopg2


conn = psycopg2.connect(database='labor_protection',
                        user='postgres', password='Liverpool',
                        host='localhost', port='5432')

# создаем объект cursor, для работы с базой данных
cur = conn.cursor()


def report_training(block_id, place_id):

    postgreSQL_select_Query = """SELECT emp.last_name || ' ' || emp.first_name || ' ' ||  emp.middle_name  as FIO,
                    pos.name as position ,
                    tr.training_date as date_of_test,
                    tr.result,
                    tr.number_document as protocol_number,
                    training_date + INTERVAL '3 years' as next_date
	FROM public.training as tr
	JOIN public.employees as emp on tr.employees_id = emp.id
	JOIN public.positions as pos on  emp.department_id = pos.id
    WHERE
    tr.block_training_id =%s"""

    cur.execute(postgreSQL_select_Query, (block_id))
    res = cur.fetchall()
    return res

def report_employees():

    postgreSQL_select_Query = """SELECT 
                    emp.zup_code as zup_code,
                    emp.last_name || ' ' || emp.first_name || ' ' ||  emp.middle_name  as FIO,
                    pos.name as position,
                    dep.name as department,
                    emp.hire_date as hire_date,
                    emp.snils as snils
	FROM public.employees as emp
	JOIN public.positions as pos on emp.position_id = pos.id
    JOIN public.departments as dep on emp.department_id = dep.id"""

    cur.execute(postgreSQL_select_Query, )
    res = cur.fetchall()
    return res


def testing_schedule(year):

    cur.execute("""SELECT emp.last_name,
                emp.first_name,
                emp.middle_name,
                pos.name,
                tr.training_date,
                tr.result,
                tr.id,
                training_date + INTERVAL '3 years' as next_date
                FROM public.training as tr
                JOIN public.employees as emp on tr.employees_id = emp.id
                JOIN public.positions as pos on  emp.department_id = pos.id
                WHERE


training_date + INTERVAL '3 years' BETWEEN date_trunc('year', % year) - interval '1 day' and date_trunc('year', % year - interval '1 year') - interval '1 day';""", (year))
    res = cur.fetchall()

    return res
