import connexion
import six

import swagger_server.service.student_service
from swagger_server.models.student import Student  # noqa: E501
from swagger_server import util
import flask

def add_student(body, subject=None):  # noqa: E501
    """Add a new student

     # noqa: E501

    :param body: Student object that needs to be added
    :type body: dict | bytes
    :param subject: The subject name
    :type subject: str

    :rtype: int
    """
    if connexion.request.is_json:
        student = Student.from_dict(connexion.request.get_json())  # noqa: E501
        return swagger_server.service.student_service.add_student(student)
        

    
    return 'do some magic!'


def delete_student(student_id):  # noqa: E501
    """delete_student

     # noqa: E501

    :param student_id: ID of student to return
    :type student_id: int

    :rtype: Student
    """

    try:
        return swagger_server.service.student_service.delete_student(student_id)
    except ValueError:
        return 'invalid id', 404


def get_student_by_id(student_id):  # noqa: E501
    """Find student by ID

    Returns a single student # noqa: E501

    :param student_id: ID of student to return
    :type student_id: int

    :rtype: Student
    """
    return swagger_server.service.student_service.get_student_by_id(student_id, '')
