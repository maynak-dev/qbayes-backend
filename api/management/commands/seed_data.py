import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from api.models import (
    TrafficSource, NewUser, SalesDistribution, Project, ProjectTask,
    ActiveAuthor, Designation, UserActivity, Location, Company, Shop,
    Role
)

class Command(BaseCommand):
    help = 'Seed the database with dummy data for dashboard'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # 1. Traffic Sources
        TrafficSource.objects.all().delete()
        sources = [
            {'name': 'Search', 'visitors': random.randint(800, 1500)},
            {'name': 'Direct', 'visitors': random.randint(300, 800)},
            {'name': 'Social', 'visitors': random.randint(200, 600)},
            {'name': 'Referral', 'visitors': random.randint(100, 400)},
            {'name': 'Email', 'visitors': random.randint(50, 300)},
        ]
        for src in sources:
            TrafficSource.objects.create(name=src['name'], visitors=src['visitors'])
        self.stdout.write('✅ Traffic sources created')

        # 2. New Users (for dashboard widget)
        NewUser.objects.all().delete()
        roles = ['HR Manager', 'Developer', 'Designer', 'Sales', 'QA Lead', 'Product Owner']
        emojis = ['👩', '👨', '🧔', '👩‍🦰', '👨‍🦱', '🧑‍💻']
        for _ in range(8):
            NewUser.objects.create(
                name=fake.name(),
                role=random.choice(roles),
                time_added=fake.date_time_between(start_date='-7d', end_date='now'),
                emoji=random.choice(emojis)
            )
        self.stdout.write('✅ New users created')

        # 3. Sales Distribution
        SalesDistribution.objects.all().delete()
        cities = ['NYC', 'LDN', 'PAR', 'TOK', 'BER']
        for city in cities:
            SalesDistribution.objects.create(city=city, sales=random.randint(1500, 10000))
        self.stdout.write('✅ Sales distribution created')

        # 4. Project & Tasks
        Project.objects.all().delete()
        project = Project.objects.create(
            name='Triton Dashboard',
            progress=random.randint(60, 90),
            due_days=random.randint(3, 10)
        )
        ProjectTask.objects.create(project=project, name='Design Phase', icon='🎨', status='Done')
        ProjectTask.objects.create(project=project, name='Development', icon='💻', status='In Progress')
        ProjectTask.objects.create(project=project, name='Testing', icon='🧪', status='Pending')
        self.stdout.write('✅ Project created')

        # 5. Active Authors
        ActiveAuthor.objects.all().delete()
        names = ['Alice M.', 'Bob D.', 'Charlie', 'Diana P.']
        roles_auth = ['Editor', 'Author', 'Reviewer', 'Writer']
        for i in range(4):
            ActiveAuthor.objects.create(
                name=names[i],
                role=roles_auth[i],
                progress=random.randint(70, 99),
                trend=random.choice(['up', 'down'])
            )
        self.stdout.write('✅ Active authors created')

        # 6. New Designations (for dashboard widget)
        Designation.objects.all().delete()
        titles = ['Senior Director', 'Product Owner', 'QA Lead', 'Compliance']
        companies_list = ['Triton Tech', 'Optitax Inc', 'Global Services', 'Finance Corp']
        colors = ['#3e97ff', '#ffc700', '#f1416c', '#50cd89']
        for i in range(4):
            Designation.objects.create(
                title=titles[i],
                company=companies_list[i],
                date=fake.date_between(start_date='-30d', end_date='today'),
                color=colors[i]
            )
        self.stdout.write('✅ New designations created')

        # 7. User Activity (monthly)
        UserActivity.objects.all().delete()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        for month in months:
            UserActivity.objects.create(
                month=month,
                active_users=random.randint(20, 40),
                new_users=random.randint(15, 45)
            )
        self.stdout.write('✅ User activity created')

        # 8. Locations (for company creation)
        Location.objects.all().delete()
        locations = []
        for _ in range(5):
            loc = Location.objects.create(name=fake.city())
            locations.append(loc)
        self.stdout.write(f'✅ Created {len(locations)} locations')

        # 9. Companies (linked to random locations)
        Company.objects.all().delete()
        companies = []
        for _ in range(8):
            comp = Company.objects.create(
                name=fake.company(),
                location=random.choice(locations) if locations else None
            )
            companies.append(comp)
        self.stdout.write(f'✅ Created {len(companies)} companies')

        # 10. Shops (linked to random companies and locations)
        Shop.objects.all().delete()
        shops = []
        for _ in range(15):
            shop = Shop.objects.create(
                name=fake.word().capitalize() + " Shop",
                company=random.choice(companies) if companies else None,
                location=random.choice(locations) if locations else None
            )
            shops.append(shop)
        self.stdout.write(f'✅ Created {len(shops)} shops')

        # 11. Roles (for Designations page)
        Role.objects.all().delete()
        role_names = [
            'HR Manager', 'Developer', 'Designer', 'Sales', 'QA Lead',
            'Product Owner', 'Senior Director', 'Compliance', 'Marketing',
            'Accountant', 'Support Engineer'
        ]
        for name in role_names:
            Role.objects.create(
                name=name,
                description=fake.sentence()
            )
        self.stdout.write(f'✅ Created {len(role_names)} roles')

        self.stdout.write(self.style.SUCCESS('🎉 Database seeded successfully!'))