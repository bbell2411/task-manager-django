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
    
    def test_user_only_sees_own_tasks(self):
        """Test user can't see other users' tasks"""
        self.client.force_authenticate(user=self.user)
        
        other_user = User.objects.create_user('other', 'other@test.com', 'pass')
        Task.objects.create(title="Not mine", user=other_user)
        Task.objects.create(title="Mine", user=self.user)
        
        response = self.client.get(reverse('task-list'))
    
        self.assertEqual(len(response.data), 1)  # Only see own task
        self.assertEqual(response.data[0]['title'], 'Mine')
    
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
    
    def test_post_task(self):
        """Test user can post their own task"""
        self.client.force_authenticate(user=self.user) 
        payload={
            "title":"new task",
            "description":"hey so this is my new task! :)"
        }
        response=self.client.post(reverse("task-list"), payload, format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"],"new task")
        self.assertEqual(response.data["user"],"testuser")
        self.assertEqual(response.data["description"],"hey so this is my new task! :)")
        self.assertIn("id",response.data)
        self.assertFalse(response.data["completed"])
        
    def test_post_task_400(self):
        """Test user cannot post if missing required fields"""
        self.client.force_authenticate(user=self.user) 
        payload={
            "description":"hey so this is my new task! :)"
        }
        response=self.client.post(reverse("task-list"), payload, format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_post_task_cannot_set_user(self):
        """Test user cannot set as a different user when posting a task"""
        self.client.force_authenticate(user=self.user) 
        other_user=User.objects.create_user('other', 'other@test.com', 'pass')
        payload = {
        "title": "Test Task",
        "user": other_user.id  
    }
        response = self.client.post(reverse('task-list'), payload)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], 'testuser')
        
    def test_post_task_invalid_completed_type(self):
        """Test invalid data type returns 400"""
        self.client.force_authenticate(user=self.user)
        
        payload = {
            "title": "Test Task",
            "completed": "not bool"  # Should be boolean
        }
        
        response = self.client.post(reverse('task-list'), payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('completed', response.data)
        
    def test_patch_task(self):
        """Test user can patch their tasks"""
        self.client.force_authenticate(user=self.user)
        task1=Task.objects.create(
            title="task1",
            description="first task",
            user=self.user
            )
        payload={
            "title":"patched task",
            "description":"i patched this task"
        }
        response=self.client.patch(reverse("task-detail", kwargs={"pk":task1.id}),payload)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["title"],"patched task")
        self.assertEqual(response.data["description"],"i patched this task")
        self.assertEqual(response.data["user"],"testuser")
        self.assertFalse(response.data["completed"])
        self.assertEqual(response.data["id"],task1.id)
        
        

        
        
        
        