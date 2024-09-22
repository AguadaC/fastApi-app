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
