from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Task

class Command(BaseCommand):
    help = 'Seeds the database with initial development data'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        user1,created=User.objects.get_or_create(
            username="John Doe",
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        
        if created:
            user1.set_password("password1")
            user1.save()
            self.stdout.write(self.style.SUCCESS(f"CREATED USER: {user1.username}"))
            
        user2,created=User.objects.get_or_create(
            username="Bell Elm",
            defaults={
                "email":"bell.elm2003@gmail.com",
                "first_name":"Bell",
                "last_name":"Elm"
            }
        )
        
        if created:
            user2.set_password("password2")
            user2.save()
            self.stdout.write(self.style.SUCCESS(f"CREATED USER: {user2.username}"))
            
            
        tasks_data = [
            {
                'title': 'Complete Django REST API',
                'description': 'Build out all endpoints for the task management system',
                'completed': False,
                'user': user1
            },
            {
                'title': 'Write API documentation',
                'description': 'Document all endpoints with request/response examples',
                'completed': False,
                'user': user1
            },
            {
                'title': 'Set up authentication',
                'description': 'Implement token-based authentication',
                'completed': True,
                'user': user1
            },
            {
                'title': 'Deploy to production',
                'description': 'Deploy the API to a cloud provider',
                'completed': False,
                'user': user2
            },
            {
                'title': 'Add pagination',
                'description': 'Implement pagination for task list endpoint',
                'completed': False,
                'user': user2
            }
        ]
        
        for task in tasks_data:
            task_data,created=Task.objects.get_or_create(
                title=task["title"],
                user=task["user"],
                defaults={
                    "description":task["description"],
                    "completed":task["completed"]
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created task: {task_data.title}'))
            
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))