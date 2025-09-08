from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task
import jsonschema

class TaskAPITest(TestCase):
    TASK_SCHEMA={
        "type":"object",
        "required":["id", "title", "completed", "user", "created_at","updated_at"],
        "properties":{
            "id":{"type":"integer"},
            "title":{"type":"string"},
            "description":{"type":["string","null"]},
            "user":{"type":"string"},
            "completed": {"type": "boolean"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at":{"type": "string", "format": "date-time"}
        }
    }
    def setUp(self):
        self.client=APIClient()
        self.user=User.objects.create(username='testuser',
            password='testpass123')
    
    def test_list_tasks(self):
        """Test user can list tasks"""
        self.client.force_authenticate(user=self.user) 
        Task.objects.create(
            title="task1",
            description="first task",
            user=self.user
            )
        Task.objects.create(
            title="task2",
            description="second task",
            user=self.user
            )
        Task.objects.create(
            title="task3",
            description="Third task",
            user=self.user
            )
        url=reverse('task-list') #finds url from viewset
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),3)
        for task in response.data:
            jsonschema.validate(task,self.TASK_SCHEMA)
    ## without json schema  ##
    # first_task = response.data[0]
    # self.assertIn('id', first_task)
    # self.assertIn('title', first_task)
    # self.assertEqual(first_task['user'], 'testuser')
    
    def test_list_tasks_unauthenticated(self):
        """Test unauthorised user gets empty list"""
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),0)
    def test_list_tasks_empty(self):
        """Test GET empty list if user has no tasks"""
        self.client.force_authenticate(user=self.user) 
        response=self.client.get(reverse("task-list"))
        self.assertEqual(response.data,[])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_get_task_by_id(self):
        """Test to get task by id"""
        self.client.force_authenticate(user=self.user) 
        task1=Task.objects.create(
            title="task1",
            description="first task",
            user=self.user
            )
        task2=Task.objects.create(
            title="task2",
            description="second task",
            user=self.user
            )
        response=self.client.get(reverse("task-detail",kwargs={"pk":task2.id}))
        data=response.data
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(data["id"],2)
        self.assertIn("id",data)
        self.assertIn("user",data)
        self.assertIn("title",data)
        self.assertFalse(data["completed"])
        self.assertEqual(data["user"],"testuser")
    def test_get_task_by_id_404(self):
        """Test NOT FOUND for GET task by id"""
        self.client.force_authenticate(user=self.user) 
        Task.objects.create(
            title="task1",
            description="first task",
            user=self.user
            )
        response=self.client.get(reverse("task-detail",kwargs={"pk":"hey"}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
        
        
        
        