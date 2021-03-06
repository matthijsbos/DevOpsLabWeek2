# coding: utf-8
from __future__ import absolute_import

import unittest
import unittest.mock

from flask import json
from six import BytesIO

from swagger_server.models.student import Student  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    @unittest.mock.patch('swagger_server.service.student_service.add_student')
    def test_add_student(self, mock_add_student):
        """Test case for add_student

        Add a new student
        """
        body = Student(first_name="test", last_name="test")
        
        mock_add_student.return_value = 99

        query_string = [('subject', 'subject_example')]
        response = self.client.open(
            '/service-api/student',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        mock_add_student.assert_called_with(body)

        jsondata = json.loads(response.data)
        
        self.assertEqual(jsondata, 99)

    @unittest.mock.patch('swagger_server.service.student_service.add_student')
    def test_add_student_already_exists(self, mock_add_student):
        """
        return 409 if student already exists
        """
        body = Student(first_name="test", last_name="test")

        mock_add_student.side_effect = ValueError

        query_string = [('subject', 'subject_example')]
        response = self.client.open(
            '/service-api/student',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        
        self.assert_status(response, 409, 
                       'Response body is : ' + response.data.decode('utf-8'))
    

    def test_add_invalid_student(self):
        """
        return 405 if student is missing first or last name
        """
        body = {
            "first_name": "test"
        }

        query_string = [('subject', 'subject_example')]
        response = self.client.open(
            '/service-api/student',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        
        self.assert_status(response, 405, 
                       'Response body is : ' + response.data.decode('utf-8'))


        body = {
            "last_name": "test"
        }

        query_string = [('subject', 'subject_example')]
        response = self.client.open(
            '/service-api/student',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        
        self.assert_status(response, 405, 
                       'Response body is : ' + response.data.decode('utf-8'))
    
    
    @unittest.mock.patch('swagger_server.service.student_service.delete_student')
    def test_delete_student(self, mock_delete_student):
        """
        Test case for delete_student
        """

        mock_student = Student(789, "first_name", "last_name", grades={})

        mock_delete_student.return_value = mock_student
        
        response = self.client.open(
            '/service-api/student/{student_id}'.format(student_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        response_student = Student.from_dict(json.loads(response.data))

        self.assertEqual(response_student, mock_student)


    @unittest.mock.patch('swagger_server.service.student_service.delete_student')
    def test_delete_student_invalid_id(self, mock_delete_student):
        """
        test delete invalid student returns 404
        """
        
        mock_delete_student.side_effect = ValueError
        
        response = self.client.open(
            '/service-api/student/{student_id}'.format(student_id=789),
            method='DELETE')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))



    @unittest.mock.patch('swagger_server.service.student_service.get_student_by_id')
    def test_get_student_by_id(self, mock_get_student_by_id):
        """Test case for get_student_by_id

        Find student by ID
        """

        mock_get_student_by_id.return_value = Student(1, "first1", "last1")

        response = self.client.open(
            '/service-api/student/{student_id}'.format(student_id=1),
            method='GET')

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        json_data = json.loads(response.data)
        print(json_data)

        self.assertEqual(json_data['student_id'], 1)
        self.assertEqual(json_data['first_name'], "first1")
        self.assertEqual(json_data['last_name'], "last1")


    @unittest.mock.patch('swagger_server.service.student_service.get_student_by_last_name')
    def test_get_student_by_last_name(self, mock_get_student_by_last_name):
        """
        find student by last name
        """

        mock_get_student_by_last_name.return_value = Student(1, "first1", "last1")

        response = self.client.open(
            '/service-api/student/?last_name={last_name}'.format(last_name='last1'),
            method='GET')

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        json_data = json.loads(response.data)
        print(json_data)

        self.assertEqual(json_data['student_id'], 1)
        self.assertEqual(json_data['first_name'], "first1")
        self.assertEqual(json_data['last_name'], "last1")


    @unittest.mock.patch('swagger_server.service.student_service.get_student_by_id')
    def test_get_student_by_id_invalid_id(self, mock_get_student_by_id):
        """
        Return 404 on invalid id
        """

        mock_get_student_by_id.side_effect = ValueError
        
        response = self.client.open(
            '/service-api/student/{student_id}'.format(student_id=1),
            method='GET')

        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        

if __name__ == '__main__':
    import unittest
    unittest.main()
