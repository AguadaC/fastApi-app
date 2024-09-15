# Data Base Structure.

## Commands to build and run

- build

```bash
docker build -t custom-postgres-image .
```

- run

```bash
docker run --name custom-postgres-container -p 5432:5432 -d custom-postgres-image
```

- enter to the container

```bash
docker exec -it custom-postgres-container psql -U postgres
```

- list data_bases: `\l`
- change data_base: `\c data_base_name`
- list tables: `\dt`

## Tables

- students: Stores information about students.
- careers: Stores information about careers.
- subjects: Stores information about subjects.
- student_career: Links students with the careers they are enrolled in.
- career_subject: Links subjects with the careers they belong to.
- subject_enrollments: Links students with specific subject enrollments within a career.


## Explanation of Each Table

### students:

- student_id: An auto-incrementing ID used as the primary key for the student.
- dni: DNI of the student.
- name: Name of the student.
- email: Optional email address of the student.
- phone: Optional phone number of the student.
- date: Automatically set date when the record is created.

### careers:

- id: An auto-incrementing ID used as the primary key for the career.
- name: Name of the career.

### subjects:

- id: An auto-incrementing ID used as the primary key for the subject.
- name: Name of the subject.

### student_career:

- student_id: References the student's ID from students.
- career_id: References the career's ID from careers.
- date: Automatically set date when the record is created.
- Composite primary key of student_id and career_id.

### subject_enrollments:

- student_id: References the student's ID from students.
- career_subject_id: References a composite key in career_subject that uniquely identifies a relationship between a career and a subject.
- date: Automatically set date when the record is created.
- Composite primary key of student_id and career_subject_id.
- Foreign key constraint on career_subject_id to ensure it references valid entries in career_subject.


## Example Queries

Insert Student

```sql
INSERT INTO students (dni, name, email, phone) VALUES ('12345678', 'John Doe', 'john.doe@example.com', '555-1234');
```

Enroll Student in Career

```sql
INSERT INTO student_career (student_id, career_id) VALUES (1, 2);
```

Link Career and Subject

```sql
INSERT INTO career_subject (career_id, subject_id) VALUES (2, 1);
```

Enroll Student in Subject

```sql
INSERT INTO subject_enrollments (student_id, career_subject_id) VALUES (1, (SELECT id FROM career_subject WHERE career_id = 2 AND subject_id = 1));
```

