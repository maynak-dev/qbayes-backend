import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import (
    TrafficSource, NewUser, SalesDistribution, Project, ProjectTask,
    ActiveAuthor, UserActivity, Company, Location, Shop, Role
)

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # 1. TrafficSources
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
        self.stdout.write('✅ Traffic sources')

        # 2. NewUsers
        NewUser.objects.all().delete()
        roles = ['HR Manager', 'Developer', 'Designer', 'Sales']
        emojis = ['👩', '👨', '🧔', '👩‍🦰']
        for _ in range(8):
            NewUser.objects.create(
                name=fake.name(),
                role=random.choice(roles),
                time_added=fake.date_time_between(start_date='-7d', end_date='now'),
                emoji=random.choice(emojis)
            )
        self.stdout.write('✅ New users')

        # 3. SalesDistribution
        SalesDistribution.objects.all().delete()
        cities = ['NYC', 'LDN', 'PAR', 'TOK', 'BER']
        for city in cities:
            SalesDistribution.objects.create(city=city, sales=random.randint(1500, 10000))
        self.stdout.write('✅ Sales distribution')

        # 4. Project & Tasks
        Project.objects.all().delete()
        project = Project.objects.create(
            name='Triton Dashboard',
            progress=random.randint(60, 90),
            due_days=random.randint(3, 10)
        )
        ProjectTask.objects.create(project=project, name='Design Phase', icon='🎨', status='Done')
        ProjectTask.objects.create(project=project, name='Development', icon='💻', status='In Progress')
        self.stdout.write('✅ Project')

        # 5. ActiveAuthors
        ActiveAuthor.objects.all().delete()
        for i in range(4):
            ActiveAuthor.objects.create(
                name=fake.name(),
                role=random.choice(['Editor', 'Author', 'Reviewer']),
                progress=random.randint(70, 99),
                trend=random.choice(['up', 'down'])
            )
        self.stdout.write('✅ Active authors')

        # 6. UserActivity
        UserActivity.objects.all().delete()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        for month in months:
            UserActivity.objects.create(
                month=month,
                active_users=random.randint(20, 40),
                new_users=random.randint(15, 45)
            )
        self.stdout.write('✅ User activity')

        # 7. Companies
        Company.objects.all().delete()
        companies = []
        for _ in range(5):
            comp = Company.objects.create(name=fake.company())
            companies.append(comp)
        self.stdout.write('✅ Companies')

        # 8. Locations (linked to companies)
        Location.objects.all().delete()
        locations = []
        for _ in range(8):
            loc = Location.objects.create(
                name=fake.city(),
                company=random.choice(companies)
            )
            locations.append(loc)
        self.stdout.write('✅ Locations')

        # 9. Shops (linked to locations)
        Shop.objects.all().delete()
        shops = []
        for _ in range(12):
            shop = Shop.objects.create(
                name=fake.word().capitalize() + ' Shop',
                location=random.choice(locations)
            )
            shops.append(shop)
        self.stdout.write('✅ Shops')

        # 10. Roles (must have non‑null company, location, shop)
        Role.objects.all().delete()
        role_data = [
            {'name': 'Admin', 'desc': 'Full system access', 'perm': True},
            {'name': 'Manager', 'desc': 'Can manage users', 'perm': True},
            {'name': 'Employee', 'desc': 'Basic user', 'perm': False},
        ]
        all_shops = list(Shop.objects.all())
        for rd in role_data:
            # pick a random shop – its location and company will be used
            shop = random.choice(all_shops)
            company = shop.location.company
            location = shop.location
            Role.objects.create(
                name=rd['name'],
                description=rd['desc'],
                company=company,
                location=location,
                shop=shop,
                role_create=rd['perm'],
                role_edit=rd['perm'],
                role_delete=rd['perm'],
                role_view=True,
                user_create=rd['perm'],
                user_edit=rd['perm'],
                user_delete=rd['perm'],
                user_view=True,
            )
        self.stdout.write('✅ Roles')
        self.stdout.write(self.style.SUCCESS('🎉 All data seeded!'))