from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from tasks.models import Task

class TaskModelTest(TestCase):
    """Test Task Model"""
    def setUp(self):
        """This runs before EACH test method"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def tearDown(self):
        """This runs after EACH test method - Django handles cleanup automatically"""
        pass
    
    def test_task_model_data_validation(self):
        """Test creating a task with all required fields"""
        
        task= Task.objects.create(
            title='Test Task',
            description='A test description',
            user=self.user
            )
        
        self.assertEqual(task.title,"Test Task")
        self.assertEqual(task.description,"A test description")
        
        self.assertEqual(task.user,self.user)
        self.assertEqual(task.user.username,"testuser")
        self.assertEqual(task.user.id, self.user.id)
        
        self.assertIsNotNone(task.id) 
        self.assertIsNotNone(task.created_at) 
        self.assertIsNotNone(task.updated_at) 
        self.assertFalse(task.completed)
        
    def test_task_ordering(self):
        """Test tasks are ordered by created_at descending"""
        task1 = Task.objects.create(title="First", user=self.user)
        task2 = Task.objects.create(title="Second", user=self.user)
        
        tasks = list(Task.objects.all())
        self.assertEqual(tasks[0], task2)  
        self.assertEqual(tasks[1], task1)
        
    def test_task_requires_user(self):
        """Test that task cannot be created without a user"""
        with self.assertRaises(IntegrityError):
            Task.objects.create(title='No User Task')
            
    def test_task_cascade_delete(self):
        """Test tasks are deleted when user is deleted"""
        task = Task.objects.create(title='Test', user=self.user)
        task_id = task.id
        
        self.user.delete()
        
        self.assertFalse(Task.objects.filter(id=task_id).exists())
    
    
    def test_task_string_representation(self):
        """Test the __str__ method"""
        task = Task.objects.create(
            title="Important Meeting",
            user=self.user
        )
        self.assertEqual(str(task), "Important Meeting")
        
        
        