-- Table for Students
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,            -- Auto-incremental ID, used as the primary key
    dni VARCHAR(20) NOT NULL,                 -- DNI of the student
    name VARCHAR(100) NOT NULL,               -- Name of the student
    email VARCHAR(100) NOT NULL,              -- Email of the student
    phone VARCHAR(20) NOT NULL,               -- Phone number of the student
    address VARCHAR(50) NOT NULL,             -- Address of the student
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Automatically set date when record is created
);

-- Table for Careers
CREATE TABLE careers (
    id SERIAL PRIMARY KEY,            -- Auto-incremental ID, used as the primary key
    name VARCHAR(100) NOT NULL        -- Name of the career
);

-- Table for Subjects
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,            -- Auto-incremental ID, used as the primary key
    name VARCHAR(100) NOT NULL,       -- Name of the subject
    class_duration INT NOT NULL       -- Duration for class in hours
);

-- Table for the many-to-many relationship between Students and Careers
CREATE TABLE student_career (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    career_id INT NOT NULL,
    year_enroll INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,  -- References the student's ID
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,            -- References the career's ID
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP                                     -- Automatically set date when record is created
);

-- Table for the many-to-many relationship between Careers and Subjects
CREATE TABLE career_subject (
    id SERIAL PRIMARY KEY,
    career_id INT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,          -- References the career's ID
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE         -- References the subject's ID
);

-- Table for the many-to-many relationship between Students and Subjects through Careers
CREATE TABLE subject_enrollments (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,                                                        -- References the student's ID
    career_subject_id INT NOT NULL,                                                 -- Composite key for career and subject
    enroll_times INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                                       -- Automatically set date when record is created
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,             
    FOREIGN KEY (career_subject_id) REFERENCES career_subject(id) ON DELETE CASCADE -- Foreign key constraint
);

-- Insert 4 students
INSERT INTO students (dni, name, email, phone, address) VALUES
('12345678', 'Alice Smith', 'alice.smith@example.com', '555-1111', 'Address 123'),
('23456789', 'Bob Johnson', 'bob.johnson@example.com', '555-2222', 'Address 234'),
('34567890', 'Carol Williams', 'carol.williams@example.com', '555-3333', 'Address 345'),
('45678901', 'David Brown', 'david.brown@example.com', '555-4444', 'Address 456');

-- Create 5 basic subjects
INSERT INTO subjects (name, class_duration) VALUES
('mathematics', 6),
('physics', 5),
('chemistry', 3),
('biology', 4),
('computer_science', 5);

-- Create 3 careers
INSERT INTO careers (name) VALUES
('electrical_engineering'),
('civil_engineering'),
('chemical_engineering');

-- Create 2 specialized subjects for each career
-- electrical_engineering
INSERT INTO subjects (name, class_duration) VALUES
('electronic_circuits', 3),
('digital_systems', 6);

-- civil_engineering
INSERT INTO subjects (name, class_duration) VALUES
('structural_analysis', 5),
('geotechnical_engineering', 4);

-- chemical_engineering
INSERT INTO subjects (name, class_duration) VALUES
('organic_chemistry', 3),
('inorganic_chemistry', 4);

-- Relate electrical_engineering to its specialized subjects
INSERT INTO career_subject (career_id, subject_id) VALUES
((SELECT id FROM careers WHERE name = 'electrical_engineering'), (SELECT id FROM subjects WHERE name = 'electronic_circuits')),
((SELECT id FROM careers WHERE name = 'electrical_engineering'), (SELECT id FROM subjects WHERE name = 'digital_systems'));

-- Relate civil_engineering to its specialized subjects
INSERT INTO career_subject (career_id, subject_id) VALUES
((SELECT id FROM careers WHERE name = 'civil_engineering'), (SELECT id FROM subjects WHERE name = 'structural_analysis')),
((SELECT id FROM careers WHERE name = 'civil_engineering'), (SELECT id FROM subjects WHERE name = 'geotechnical_engineering'));

-- Relate chemical_engineering to its specialized subjects
INSERT INTO career_subject (career_id, subject_id) VALUES
((SELECT id FROM careers WHERE name = 'chemical_engineering'), (SELECT id FROM subjects WHERE name = 'organic_chemistry')),
((SELECT id FROM careers WHERE name = 'chemical_engineering'), (SELECT id FROM subjects WHERE name = 'inorganic_chemistry'));

-- Relate electrical_engineering to 3 basic subjects
INSERT INTO career_subject (career_id, subject_id) VALUES
((SELECT id FROM careers WHERE name = 'electrical_engineering'), (SELECT id FROM subjects WHERE name = 'mathematics')),
((SELECT id FROM careers WHERE name = 'electrical_engineering'), (SELECT id FROM subjects WHERE name = 'physics')),
((SELECT id FROM careers WHERE name = 'electrical_engineering'), (SELECT id FROM subjects WHERE name = 'computer_science'));

-- Relate civil_engineering to 3 basic subjects
INSERT INTO career_subject (career_id, subject_id) VALUES
((SELECT id FROM careers WHERE name = 'civil_engineering'), (SELECT id FROM subjects WHERE name = 'mathematics')),
((SELECT id FROM careers WHERE name = 'civil_engineering'), (SELECT id FROM subjects WHERE name = 'physics')),
((SELECT id FROM careers WHERE name = 'civil_engineering'), (SELECT id FROM subjects WHERE name = 'chemistry'));

-- Relate chemical_engineering to 3 basic subjects
INSERT INTO career_subject (career_id, subject_id) VALUES
((SELECT id FROM careers WHERE name = 'chemical_engineering'), (SELECT id FROM subjects WHERE name = 'mathematics')),
((SELECT id FROM careers WHERE name = 'chemical_engineering'), (SELECT id FROM subjects WHERE name = 'chemistry')),
((SELECT id FROM careers WHERE name = 'chemical_engineering'), (SELECT id FROM subjects WHERE name = 'biology'));
