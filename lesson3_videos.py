import os
# usually you will see from peewee import *
import peewee as pw
from loguru import logger

file = 'personjob.db'
if os.path.exists(file):
    os.remove(file)

db = pw.SqliteDatabase(file)


class BaseModel(pw.Model):
    logger.info("allows database to be defined changed) in one place")

    class Meta:
        database = db


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info("notice peewee data type")

    person_name = pw.CharField(primary_key=True, max_length=30)
    lives_in_town = pw.CharField(max_length=40)
    nickname = pw.CharField(max_length=20, null=True)

    logger.info("can add methods too")

    def show(self):
        """ display an instance """
        print(self.person_name, self.lives_in_town, self.nickname)


class Department(BaseModel):
    """
        This class defines Department, which maintains details of in
        which Department a Person held a Job
    """

    dept_number = pw.CharField(max_length=30)
    dept_name = pw.CharField(primary_key=True, max_length=30)
    dept_manager = pw.ForeignKeyField(Person, related_name='person', null=False)

    def show(self):
        """ display an instance """
        print(self.dept_number, self.dept_name, self.dept_manager)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    job_name = pw.CharField(primary_key=True, max_length=30)
    start_date = pw.DateField(formats='YYYY-MM-DD')
    end_date = pw.DateField(formats='YYYY-MM-DD')

    salary = pw.DecimalField(max_digits=7, decimal_places=2)
    person_employed = pw.ForeignKeyField(
        Person, related_name='was_filled_by', null=False)
    dept_name_for_job = pw.ForeignKeyField(Department, related_name='related_dept_name', null=False)

    def show(self):
        """ display an instance """
        print(self.job_name, self.start_date, self.end_date, self.salary, self.person_employed, self.dept_name_for_job)

def main():
    """ add and print some records """
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    db.create_tables([
        Person,
        Department,
        Job
    ])

    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', None),
        ('Susan', 'Boston', 'Beannie'),
        ('Steven', 'Colchester', None),
        ('Peter', 'Seattle', None),
    ]

    for person in people:
        try:
            with db.transaction():
                new_person = Person.create(
                    person_name=person[0],
                    lives_in_town=person[1],
                    nickname=person[2], )
                new_person.save()

        except Exception as e:
            logger.info(f'Error creating person = {person[0]}')
            logger.info(e)
            logger.info('See how the datbase protects our data')

    for person in Person:
        person.show()

    depts = [
        ('A101', 'Flight Controls', 'Andrew'),
        ('B245', 'Stability and Control', 'Peter'),
        ('Q456', 'Advanced Research', 'Susan'),
        ('1234', 'Dept of bad naming conventions', 'Steven'),
        ('C12345', 'Dept of too long numbers', 'Peter')
    ]

    for dept in depts:
        try:
            with db.transaction():
                new_dept = Department.create(
                    dept_number=dept[0],
                    dept_name=dept[1],
                    dept_manager=dept[2], )
                new_dept.save()

        except Exception as e:
            logger.info(f'Error creating department = {dept[0]}')
            logger.info(e)
            logger.info('Database protects adding department when a person does not exist for it')

    for dept in Department:
        dept.show()

    jobs = [
        ('Analyst', '2017-02-01', '2019-07-31', 34.999, 'Andrew', 'Flight Controls'),
        ('Developer', '2017-02-01', '2019-07-31', 34.999, 'Fred', 'Advanced Research'),
    ]

    for job in jobs:
        try:
            with db.transaction():
                new_job = Job.create(
                    job_name=job[0],
                    start_date=job[1],
                    end_date=job[2],
                    salary=job[3],
                    person_employed=job[4],
                    dept_name_for_job=job[5], )
                new_job.save()

                # query_job_details = Job.select().where(Job.job_name == job)
                # dur_job_held = query_job_details.end_date - query_job_details.start_date

        except Exception as e:
            logger.info(f'Error creating job = {job[0]}')
            logger.info(e)
            logger.info('See how the datbase protects data across tables')

    for job in Job:
        job.show()

    # logger.info("don't forget - but can you find a better way?")
    db.close()


if __name__ == "__main__":
    main()
