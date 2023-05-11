SELECT * FROM students_info.students_info;

-- Students residing from Laguna -- 
SELECT * FROM students_info.students_info where city = 'Laguna';

-- Students with a semestral grade of 80 -- 
SELECT * FROM students_info.students_info where sem_grade = '80';

-- Students who are female -- 
SELECT * FROM students_info.students_info where gender = 'F';

-- Students who are the youngest -- 
SELECT min(entry_age) FROM students_info.students_info;
SELECT * FROM students_info.students_info where entry_age = 17;

-- Students with the highest final exam -- 
SELECT max(final_exam) FROM students_info.students_info;
SELECT * FROM students_info.students_info where final_exam = 100;

-- Students who are not in 4th Year -- 
SELECT * FROM students_info.students_info where not status = '4TH YEAR' order by status desc;

-- Students arranged by semestral grade -- 
SELECT * FROM students_info.students_info order by sem_grade desc;

-- Students who are male and in 1st Year -- 
SELECT * FROM students_info.students_info where gender = 'M' and status = '1ST YEAR';
