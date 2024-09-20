# -*- coding: utf-8 -*-
"""SQL Models module."""

from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func


Base = declarative_base()

# Model for Students
class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    date = Column(TIMESTAMP, server_default=func.now())

    careers = relationship('StudentCareer', back_populates='student', cascade='all, delete-orphan')
    enrollments = relationship('SubjectEnrollment', back_populates='student', cascade='all, delete-orphan')

# Model for Careers
class Career(Base):
    __tablename__ = 'careers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)


    students = relationship('StudentCareer', back_populates='career', cascade='all, delete-orphan')
    subjects = relationship('CareerSubject', back_populates='career', cascade='all, delete-orphan')

# Model for Subjects
class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)


    careers = relationship('CareerSubject', back_populates='subject', cascade='all, delete-orphan')

# Model for Students and Careers
class StudentCareer(Base):
    __tablename__ = 'student_career'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), primary_key=True)
    career_id = Column(Integer, ForeignKey('careers.id', ondelete='CASCADE'), primary_key=True)
    date = Column(TIMESTAMP, server_default=func.now())

    student = relationship('Student', back_populates='careers')
    career = relationship('Career', back_populates='students')

# Model for Careers and Subjects
class CareerSubject(Base):
    __tablename__ = 'career_subject'

    id = Column(Integer, primary_key=True, autoincrement=True)
    career_id = Column(Integer, ForeignKey('careers.id', ondelete='CASCADE'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True)

    career = relationship('Career', back_populates='subjects')
    subject = relationship('Subject', back_populates='careers')
    enrollments = relationship('SubjectEnrollment', back_populates='career_subject')

# Model for Subjects through Careers
class SubjectEnrollment(Base):
    __tablename__ = 'subject_enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    career_subject_id = Column(Integer, ForeignKey('career_subject.id', ondelete='CASCADE'), nullable=False)
    date = Column(TIMESTAMP, server_default=func.now())

    career_subject = relationship('CareerSubject', back_populates='enrollments')
    student = relationship('Student', back_populates='enrollments')
