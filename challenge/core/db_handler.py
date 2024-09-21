# -*- coding: utf-8 -*-
"""DB Handler module."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from typing import List, Optional

from challenge import settings
from challenge.core.log_manager import LogManager
from challenge.exceptions import (StudentDoesNotExist,
                                  CareerDoesNotExist,
                                  UnenrolledStudent,
                                  SubjectDoesNotExist,
                                  CareerSubjectDoesNotExist,
                                  EnrollRecordDoesNotExist)
from challenge.models.sql_models import (Student,
                                         Career,
                                         Subject,
                                         StudentCareer,
                                         CareerSubject,
                                         SubjectEnrollment)
from challenge.models.api_models import RetriveLeadRecord

logger = LogManager().logger()

class DbHandler:
    """Class to manage transfers with the db"""

    def __init__(self):
        """
        Initialize the DbHandler instance with database connection settings.
        Sets up the asynchronous engine and sessionmaker for interacting with the database.
        """
        self._database_url = (
            'postgresql+asyncpg://'
            f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
            f'@{settings.POSTGRES_HOST}:5432/{settings.POSTGRES_DB}'
        )
        self._engine = create_async_engine(self._database_url, echo=settings.POSTGRES_ECHO)
        self._SessionLocal = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def create_student(self,
                             dni: str,
                             name: str,
                             email: Optional[str] = None,
                             phone: Optional[str] = None,
                             address: Optional[str] = None
                             ) -> int:
        """
        Create a new student record in the database.

        Args:
            dni (str): The DNI of the student.
            name (str): The name of the student.
            email (Optional[str]): The optional email of the student.
            phone (Optional[str]): The optional phone number of the student.
            address (Optional[str]): The optional address of the student.

        Returns:
            student_id (int): The ID of the student.
        """
        async with self._SessionLocal() as session:
            async with session.begin():
                new_student = Student(dni=dni,
                                      name=name,
                                      email=email,
                                      phone=phone,
                                      address=address)
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
        Retrieve a student record by its unique ID.

        Args:
            student_id (int): The unique identifier of the student.

        Raises:
            StudentDoesNotExist: If no student is found with the given ID.

        Returns:
            Student: The student record associated with the provided ID.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Student).where(Student.student_id == student_id)
            )
            student = result.scalars().first()
            if not student:
                raise StudentDoesNotExist(f"No Student with ID: {student_id}")
        return student

    async def enroll_student_in_a_career(self,
                                         student_id: int,
                                         career_id: int,
                                         year_enroll: int) -> int:
        """
        Enroll a student in a specific career for a given year.

        Args:
            student_id (int): The unique identifier of the student to enroll.
            career_id (int): The unique identifier of the career to enroll the student in.
            year_enroll (int): The year in which the student is enrolling.

        Returns:
            int: The unique identifier of the newly created enrollment record.
        """
        async with self._SessionLocal() as session:
            async with session.begin():
                new_enrollment = StudentCareer(student_id=student_id,
                                               career_id=career_id,
                                               year_enroll=year_enroll)
                session.add(new_enrollment)
                await session.flush()
                enrollment_id = new_enrollment.id
            await session.commit()
            return enrollment_id

    async def enroll_student_in_a_subject(self,
                                          student_id: int,
                                          career_subject_id: int,
                                          enroll_times: int
                                          ) -> int:
        """
        Enroll a student in a specific subject for a given number of enrollments.

        Args:
            student_id (int): The unique identifier of the student to enroll.
            career_subject_id (int): The unique identifier of the career subject the student is enrolling in.
            enroll_times (int): The number of times the student is enrolling in the subject.

        Returns:
            int: The unique identifier of the newly created subject enrollment record.
        """
        async with self._SessionLocal() as session:
            async with session.begin():
                new_enrollment = SubjectEnrollment(
                    student_id=student_id,
                    career_subject_id=career_subject_id,
                    enroll_times = enroll_times
                )
                session.add(new_enrollment)
                await session.flush()
                enrollment_id = new_enrollment.id
            await session.commit()
            return enrollment_id

    async def _get_student_id_by_dni(self, dni: str) -> Optional[int]:
        """
        Retrieve the unique identifier of a student based on their DNI (National Identity Document).

        Args:
            dni (str): The DNI of the student whose ID is to be retrieved.

        Returns:
            Optional[int]: The unique identifier of the student if found; otherwise, raises an exception.

        Raises:
            StudentDoesNotExist: If no student with the given DNI exists in the database.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Student.student_id).filter_by(dni=dni)
            )
            student_id = result.scalar_one_or_none()
            if not student_id:
                raise StudentDoesNotExist(f"No Student with DNI: {dni}")
            return student_id

    async def _get_career_id_by_name(self, name: str) -> Optional[int]:
        """
        Retrieve the ID of a career based on its name.

        Args:
            name (str): The name of the career to search for.

        Returns:
            Optional[int]: The ID of the career if found.
        
        Raises:
            CareerDoesNotExist: If no career with the specified name is found in the database.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Career.id).filter_by(name=name)
            )
            career_id = result.scalar_one_or_none()
            if not career_id:
                raise CareerDoesNotExist(f"No Career with name: {name}")
            return career_id

    async def _get_subject_id_by_name(self, subject_name: str) -> Optional[int]:
        """
        Retrieve the ID of a subject based on its name.

        Args:
            subject_name (str): The name of the subject to search for.

        Returns:
            Optional[int]: The ID of the subject if found.
        
        Raises:
            SubjectDoesNotExist: If no subject with the specified name is found in the database.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Subject.id).filter_by(name=subject_name)
            )
            subject_id = result.scalar_one_or_none()
            if not subject_id:
                raise SubjectDoesNotExist(f"No Subject with name: {subject_name}")
            return subject_id

    async def _get_career_subject_id(self,
                                     career_id: int,
                                     subject_id: int
                                     ) -> Optional[int]:
        """
        Retrieve the ID of a career-subject relationship based on the career and subject IDs.

        Args:
            career_id (int): The ID of the career to search for.
            subject_id (int): The ID of the subject to search for.

        Returns:
            Optional[int]: The ID of the career-subject relationship if found.

        Raises:
            CareerSubjectDoesNotExist: If the specified subject is not related to the specified career.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(CareerSubject.id).filter_by(
                    career_id=career_id,
                    subject_id=subject_id
                )
            )
            career_subject_id = result.scalar_one_or_none()
            if not career_subject_id:
                raise CareerSubjectDoesNotExist(f"Subject is not related with the career.")
            return career_subject_id

    async def _get_subject_enrollment_id(self,
                                         student_id: int,
                                         career_subject_id: int,
                                         enroll_times: int
                                         ) -> Optional[int]:
        """
        Retrieve the ID of a subject enrollment based on student ID, career-subject ID, and enrollment times.

        Args:
            student_id (int): The ID of the student whose enrollment is being checked.
            career_subject_id (int): The ID of the career-subject relationship.
            enroll_times (int): The number of times the student is enrolled in the subject.

        Returns:
            Optional[int]: The ID of the subject enrollment if found.

        Raises:
            UnenrolledStudent: If the specified student is not enrolled in the subject.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(SubjectEnrollment.id).filter_by(
                    student_id=student_id,
                    career_subject_id=career_subject_id,
                    enroll_times=enroll_times
                )
            )
            subject_enrollment_id = result.scalar_one_or_none()
            if not subject_enrollment_id:
                raise UnenrolledStudent(f"Student in not enrolled in the subject")
            return subject_enrollment_id
    
    async def _get_subject_enrollment_by_id(self,
                                         id: int,
                                         ) -> Optional[SubjectEnrollment]:
        """
        Retrieve a subject enrollment record by its ID.

        Args:
            id (int): The ID of the subject enrollment record to retrieve.

        Returns:
            Optional[SubjectEnrollment]: The subject enrollment record if found.
        Raises:
            EnrollRecordDoesNotExist: If no subject enrollment record exists for the specified ID.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(SubjectEnrollment).where(
                    SubjectEnrollment.id == id
                )
            )
            subject_enrollment = result.scalars().first()
            if not subject_enrollment:
                raise EnrollRecordDoesNotExist(f"Record with ID:{id} does not exist")
            return subject_enrollment

    async def _get_career_subject_by_id(self,
                                         id: int,
                                         ) -> Optional[CareerSubject]:
        """
        Retrieve a career-subject relationship record by its ID.

        Args:
            id (int): The ID of the career-subject record to retrieve.

        Returns:
            Optional[CareerSubject]: The career-subject record if found; otherwise, returns None.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(CareerSubject).where(
                    CareerSubject.id == id
                )
            )
            carrer_subject= result.scalars().first()
            return carrer_subject

    async def _get_career_by_id(self,
                                id: int,
                                ) -> Optional[Career]:
        """
        Retrieve a career record by its ID.

        Args:
            id (int): The ID of the career record to retrieve.

        Returns:
            Optional[Career]: The career record if found; otherwise, returns None.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Career).where(
                    Career.id == id
                )
            )
            carrer= result.scalars().first()
            return carrer

    async def _get_subject_by_id(self,
                                id: int,
                                ) -> Optional[Subject]:
        """
        Retrieve a subject record by its ID.

        Args:
            id (int): The ID of the subject record to retrieve.

        Returns:
            Optional[Subject]: The subject record if found; otherwise, returns None.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(Subject).where(
                    Subject.id == id
                )
            )
            subject= result.scalars().first()
            return subject

    async def _get_student_career_by_ids(self,
                                        student_id: int,
                                        career_id: int,
                                        ) -> Optional[StudentCareer]:
        """
        Retrieve a student's career record by student ID and career ID.

        Args:
            student_id (int): The ID of the student.
            career_id (int): The ID of the career.

        Returns:
            Optional[StudentCareer]: The student's career record if found; otherwise, raises UnenrolledStudent.
        
        Raises:
            UnenrolledStudent: If the student is not enrolled in the specified career.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(
                select(StudentCareer).where(
                    StudentCareer.student_id == student_id,
                    StudentCareer.career_id == career_id
                )
            )
            student_career = result.scalar_one_or_none()
            if not student_career:
                raise UnenrolledStudent(f"Student in not enrolled in the subject")
            return student_career

    async def _get_all_record_ids(self) -> List[SubjectEnrollment]:
        """
        Retrieve all subject enrollment record IDs.

        This function queries the database for all IDs associated with 
        subject enrollment records and returns them as a list.

        Returns:
            List[SubjectEnrollment]: A list of IDs of all subject enrollment records.
        """
        async with self._SessionLocal() as session:
            result = await session.execute(select(SubjectEnrollment.id))
            query_list = list()
            for subject_enroll_record in result:
                query_list.append(subject_enroll_record[0])
        return query_list

    async def _build_record_by_id(self, record_id: int) -> RetriveLeadRecord:
        """
        Build a lead record by its subject enrollment ID.

        This function retrieves the subject enrollment record and related
        student, career, and subject information based on the provided
        record ID. It constructs and returns a `RetriveLeadRecord` object
        populated with the relevant data.

        Args:
            record_id (int): The ID of the subject enrollment record.

        Returns:
            RetriveLeadRecord: An object containing the details of the
            lead record, including student information, subject details,
            and enrollment information.
        """
        record = await self._get_subject_enrollment_by_id(id=record_id)
        student_obj = await self.get_student_by_id(record.student_id)
        career_subject_obj = await self._get_career_subject_by_id(record.career_subject_id)
        career_obj = await self._get_career_by_id(career_subject_obj.career_id)
        student_career_obj = await self._get_student_career_by_ids(student_obj.student_id,
                                                                        career_obj.id)
        subject_obj = await self._get_subject_by_id(career_subject_obj.subject_id)
        return RetriveLeadRecord(id=record_id,
                                dni=student_obj.dni,
                                name=student_obj.name,
                                email=student_obj.email,
                                phone=student_obj.phone,
                                address=student_obj.address,
                                subject=subject_obj.name,
                                class_duration=subject_obj.class_duration,
                                enroll_times=record.enroll_times,
                                career=career_obj.name,
                                year_enroll=student_career_obj.year_enroll)
