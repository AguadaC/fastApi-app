# -*- coding: utf-8 -*-
"""DB Handler module."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import List, Optional

from challenge import settings
from challenge.models.sql_models import (Student,
                                         Career,
                                         Subject,
                                         StudentCareer,
                                         CareerSubject,
                                         SubjectEnrollment)


class DbHandler:
    """Class to manage db transfers"""

    def __init__(self):
        """
        Initialize the DbHandler instance with database connection settings.
        Sets up the asynchronous engine and sessionmaker for interacting with the database.
        """
        self._database_url = (
            'postgresql+asyncpg://'
            f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
            f'@localhost:5432/{settings.POSTGRES_DB}'
        )
        self._engine = create_async_engine(self._database_url, echo=settings.ECHO)
        self._SessionLocal = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def create_student(self,
                             dni: str,
                             name: str,
                             email: Optional[str] = None,
                             phone: Optional[str] = None
                             ) -> int:
        """
        Create a new student record in the database.

        Args:
            dni (str): The DNI of the student.
            name (str): The name of the student.
            email (Optional[str]): The optional email of the student.
            phone (Optional[str]): The optional phone number of the student.

        Returns:
            student_id (int): The ID of the student (either existing or newly created).
        """
        async with self._SessionLocal() as session:
            async with session.begin():
                student_id_exists = await self._get_student_id_by_dni(dni=dni)
                if student_id_exists:
                    return student_id_exists
                new_student = Student(dni=dni, name=name, email=email, phone=phone)
                session.add(new_student)
                await session.flush()
                student_id = new_student.student_id
            await session.commit()
        return student_id

    async def get_all_students(self) -> List[Student]:
        """
        Retrieve all student records from the database.

        Returns:
            List[Student]: A list of all students.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(select(Student))
            query_list = list()
            for student_tuple in result:
                query_list.append(student_tuple[0])
        return query_list

    async def get_student_by_id(self, student_id) -> Student:
        """
        Retrieve the student record from the database by ID.

        Returns:
            Student: Student based on ID.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Student).where(Student.student_id == student_id)
            )
            student = result.scalars().first()
        return student

    async def enroll_student_in_a_career(self, dni: str, career_name: str) -> int:
        """
        Enroll a student in a career. If the student is already enrolled, return the existing enrollment ID.
        If not, create a new enrollment and return the new enrollment ID.

        Args:
            dni (str): The DNI of the student to enroll.
            career_name (str): The name of the career to enroll the student in.

        Returns:
            enrollment_id (int): The ID of the enrollment (either existing or newly created).
        """
        async with self._SessionLocal() as session:
            async with session.begin():
                student_career_id = await self._get_student_career_id(dni=dni,
                                                                      career_name=career_name)
                if student_career_id:
                    return student_career_id

                student_id = await self._get_student_id_by_dni(dni=dni)
                career_id = await self._get_career_id_by_name(name=career_name)
                new_enrollment = StudentCareer(student_id=student_id, career_id=career_id)
                session.add(new_enrollment)
                await session.flush()
                enrollment_id = new_enrollment.id
            await session.commit()
            return enrollment_id

    async def enroll_student_in_a_subject(self,
                                          dni: str,
                                          career_name: str,
                                          subject_name: str
                                          ) -> int:
            """
            Enroll a student in a subject if they are enrolled in the associated career
            and the subject is part of that career.

            Args:
                dni (str): The DNI of the student.
                career_name (str): The name of the career to which the subject is associated.
                subject_name (str): The name of the subject to enroll the student in.

            Returns:
                int: The ID of the enrollment (either existing or newly created).
            """
            async with self._SessionLocal() as session:
                async with session.begin():
                    existing_enrollment = await self._get_subject_enrollment_id(
                        dni=dni,
                        career_name=career_name,
                        subject_name=subject_name
                    )
                    if existing_enrollment:
                        return existing_enrollment

                    enrolled = await self._get_student_career_id(dni=dni,
                                                                 career_name=career_name)
                    if enrolled:
                        career_subject_id = await self._get_career_subject_id(career_name=career_name,
                                                                              subject_name=subject_name)
                        if career_subject_id:
                            student_id = await self._get_student_id_by_dni(dni=dni)

                            new_enrollment = SubjectEnrollment(
                                student_id=student_id,
                                career_subject_id=career_subject_id
                            )
                            session.add(new_enrollment)
                            await session.flush()
                            enrollment_id = new_enrollment.id
                await session.commit()
                return enrollment_id

    async def _get_student_id_by_dni(self, dni: str) -> Optional[int]:
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Student.student_id).filter_by(dni=dni)
            )
            student_id = result.scalar_one_or_none()
            return student_id

    async def _get_career_id_by_name(self, name: str) -> Optional[int]:
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Career.id).filter_by(name=name)
            )
            career_id = result.scalar_one_or_none()
            return career_id

    async def _get_subject_id_by_name(self, name: str) -> Optional[int]:
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Subject.id).filter_by(name=name)
            )
            subject_id = result.scalar_one_or_none()
            return subject_id

    async def _get_student_career_id(self, dni: str, career_name: str) -> Optional[int]:
        async with self._SessionLocal() as session:
            student_id = await self._get_student_id_by_dni(dni)
            if student_id is None:
                return None
            career_id = await self._get_career_id_by_name(career_name)
            if career_id is None:
                return None
            result = await session.execute(
                select(StudentCareer.id).filter_by(
                    student_id=student_id,
                    career_id=career_id
                )
            )
            student_career_id = result.scalar_one_or_none()
            return student_career_id

    async def _get_career_subject_id(self, career_name: str, subject_name: str) -> Optional[int]:
        async with self._SessionLocal() as session:
            career_id = await self._get_career_id_by_name(career_name)
            if career_id is None:
                return None
            subject_id = await self._get_subject_id_by_name(subject_name)
            if subject_id is None:
                return None
            result = await session.execute(
                select(CareerSubject.id).filter_by(
                    career_id=career_id,
                    subject_id=subject_id
                )
            )
            career_subject_id = result.scalar_one_or_none()
            return career_subject_id

    async def _get_subject_enrollment_id(self,
                                         dni: str,
                                         career_name: str,
                                         subject_name: str
                                         ) -> Optional[int]:
        async with self._SessionLocal() as session:
            student_career_id = await self._get_student_career_id(dni, career_name)
            if student_career_id is None:
                return None
            career_subject_id = await self._get_career_subject_id(career_name, subject_name)
            if career_subject_id is None:
                return None
            result = await session.execute(
                select(SubjectEnrollment.id).filter_by(
                    student_id=student_career_id,
                    career_subject_id=career_subject_id
                )
            )
            subject_enrollment_id = result.scalar_one_or_none()
            return subject_enrollment_id
