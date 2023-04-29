create schema exercise;

create table exercise.emp_1
(EMP_NUM CHAR(3),
EMP_LNAME VARCHAR(15),
EMP_FNAME VARCHAR(15),
EMP_INITIAL CHAR(1),
EMP_HIREDATE DATE,
JOB_CODE CHAR(3));

insert into exercise.emp_1(EMP_NUM, EMP_LNAME, EMP_FNAME, EMP_INITIAL, EMP_HIREDATE, JOB_CODE)
values ('1', 'Silleza', 'Miguel', ' ', '2023-04-08', '502');

select * from exercise.emp_1
where JOB_CODE = '502';