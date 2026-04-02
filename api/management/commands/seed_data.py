import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from api.models import (
    Company, Location, Shop, Role, Profile,
    TrafficSource, NewUser, SalesDistribution, Project,
    ProjectTask, ActiveAuthor, UserActivity, Designation,
    Jewellery, RFID, RFIDJewelleryMap
)

class Command(BaseCommand):
    help = 'Seed database with realistic data without deleting existing records'

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write('Seeding data...')

        # 1. Companies
        if Company.objects.count() < 5:
            for _ in range(5 - Company.objects.count()):
                Company.objects.create(name=fake.unique.company())
        companies = list(Company.objects.all()[:5])
        self.stdout.write(f'✅ Using {len(companies)} companies')

        # 2. Locations
        for company in companies:
            needed = max(0, random.randint(2, 4) - company.locations.count())
            for _ in range(needed):
                Location.objects.create(
                    name=fake.unique.city(),
                    company=company
                )
        locations = list(Location.objects.filter(company__in=companies))
        self.stdout.write(f'✅ Using {len(locations)} locations')

        # 3. Shops
        for location in locations:
            needed = max(0, random.randint(1, 3) - location.shops.count())
            for _ in range(needed):
                Shop.objects.create(
                    name=fake.unique.word().capitalize() + " Shop",
                    location=location
                )
        shops = list(Shop.objects.filter(location__in=locations))
        self.stdout.write(f'✅ Using {len(shops)} shops')

        # 4. Roles (create if not exist)
        role_data = [
            ('Admin', True),
            ('Manager', True),
            ('Employee', False),
            ('HR', True),
            ('Sales', False),
        ]
        roles = []
        for name, has_perm in role_data:
            role, created = Role.objects.get_or_create(
                name=name,
                defaults={
                    'description': fake.sentence(),
                    'company': random.choice(companies),
                    'location': random.choice(locations),
                    'shop': random.choice(shops),
                    'role_create': has_perm,
                    'role_edit': has_perm,
                    'role_delete': has_perm,
                    'role_view': True,
                    'user_create': has_perm,
                    'user_edit': has_perm,
                    'user_delete': has_perm,
                    'user_view': True,
                }
            )
            roles.append(role)
        self.stdout.write(f'✅ Using {len(roles)} roles')

        # 5. New users with profiles
        new_users = []
        for _ in range(10):
            username = fake.unique.user_name()
            email = fake.unique.email()
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            new_users.append(user)
        self.stdout.write(f'✅ Created {len(new_users)} new users')

        # 6. Profiles for new users (with phone truncated to 20 chars)
        for user in new_users:
            role = random.choice(roles)
            # Truncate phone number to fit max_length=20
            phone = fake.phone_number()[:20]
            Profile.objects.create(
                user=user,
                role=role,
                phone=phone,
                status=random.choice(['Pending', 'Approved', 'Rejected']),
                steps=random.randint(0, 10),
                company=role.company.name,
                location=role.location.name,
                shop=role.shop.name,
            )
        self.stdout.write('✅ Created profiles for new users')

        # 7. Dashboard models (only if missing)
        # TrafficSource
        if TrafficSource.objects.count() == 0:
            for src in [
                {'name': 'Search', 'visitors': random.randint(800, 1500)},
                {'name': 'Direct', 'visitors': random.randint(300, 800)},
                {'name': 'Social', 'visitors': random.randint(200, 600)},
                {'name': 'Referral', 'visitors': random.randint(100, 400)},
                {'name': 'Email', 'visitors': random.randint(50, 300)},
            ]:
                TrafficSource.objects.create(**src)
            self.stdout.write('✅ Traffic sources created')
        else:
            self.stdout.write('✅ Traffic sources already exist')

        # NewUser widget
        if NewUser.objects.count() < 8:
            roles_list = ['HR Manager', 'Developer', 'Designer', 'Sales']
            emojis = ['👩', '👨', '🧔', '👩‍🦰']
            for _ in range(8 - NewUser.objects.count()):
                NewUser.objects.create(
                    name=fake.name(),
                    role=random.choice(roles_list),
                    time_added=fake.date_time_between(start_date='-7d', end_date='now'),
                    emoji=random.choice(emojis)
                )
            self.stdout.write('✅ New users widget seeded')
        else:
            self.stdout.write('✅ New users widget already has data')

        # SalesDistribution
        if SalesDistribution.objects.count() == 0:
            for city in ['NYC', 'LDN', 'PAR', 'TOK', 'BER']:
                SalesDistribution.objects.create(city=city, sales=random.randint(1500, 10000))
            self.stdout.write('✅ Sales distribution created')
        else:
            self.stdout.write('✅ Sales distribution already exists')

        # Project & Tasks
        if Project.objects.count() == 0:
            project = Project.objects.create(
                name='Triton Dashboard',
                progress=random.randint(60, 90),
                due_days=random.randint(3, 10)
            )
            ProjectTask.objects.create(project=project, name='Design Phase', icon='🎨', status='Done')
            ProjectTask.objects.create(project=project, name='Development', icon='💻', status='In Progress')
            self.stdout.write('✅ Project created')
        else:
            self.stdout.write('✅ Project already exists')

        # ActiveAuthor
        if ActiveAuthor.objects.count() < 4:
            for _ in range(4 - ActiveAuthor.objects.count()):
                ActiveAuthor.objects.create(
                    name=fake.name(),
                    role=random.choice(['Editor', 'Author', 'Reviewer']),
                    progress=random.randint(70, 99),
                    trend=random.choice(['up', 'down'])
                )
            self.stdout.write('✅ Active authors seeded')
        else:
            self.stdout.write('✅ Active authors already have data')

        # UserActivity
        if UserActivity.objects.count() == 0:
            for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']:
                UserActivity.objects.create(
                    month=month,
                    active_users=random.randint(20, 40),
                    new_users=random.randint(15, 45)
                )
            self.stdout.write('✅ User activity created')
        else:
            self.stdout.write('✅ User activity already exists')

        # Designations (optional)
        if Designation.objects.count() == 0:
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
            self.stdout.write('✅ Designations created')
        else:
            self.stdout.write('✅ Designations already exist')

        # 8. Jewellery
        if Jewellery.objects.count() == 0:
            jewellery_items = []
            for _ in range(20):
                jew = Jewellery.objects.create(
                    jewellery_id=f"J{random.randint(1000,9999)}",
                    design_number=f"D{random.randint(100,999)}",
                    collection_type=random.choice(['Gold', 'Platinum', 'Silver']),
                    metal_type=random.choice(['Yellow Gold', 'White Gold', 'Rose Gold']),
                    category=random.choice(['Ring', 'Necklace', 'Earring', 'Bracelet']),
                    sub_category=random.choice(['Engagement', 'Wedding', 'Casual']),
                    status=random.choice(['active', 'inactive']),
                    added_by=random.choice(new_users) if new_users else None
                )
                jewellery_items.append(jew)
            self.stdout.write(f'✅ Created {len(jewellery_items)} jewellery items')
        else:
            self.stdout.write('✅ Jewellery already exists')

        # 9. RFID
        if RFID.objects.count() == 0:
            rfid_items = []
            for _ in range(30):
                rfid = RFID.objects.create(
                    tag=f"RFID-{random.randint(10000,99999)}",
                    status=random.choice(['active', 'inactive']),
                    added_by=random.choice(new_users) if new_users else None
                )
                rfid_items.append(rfid)
            self.stdout.write(f'✅ Created {len(rfid_items)} RFID tags')
        else:
            self.stdout.write('✅ RFID already exists')

        # 10. RFIDJewelleryMap
        if RFIDJewelleryMap.objects.count() == 0:
            all_jewellery = list(Jewellery.objects.all())
            all_rfid = list(RFID.objects.all())
            if all_jewellery and all_rfid:
                maps_created = 0
                for _ in range(15):
                    try:
                        RFIDJewelleryMap.objects.create(
                            jewellery=random.choice(all_jewellery),
                            rfid=random.choice(all_rfid),
                            status=random.choice(['active', 'inactive']),
                            added_by=random.choice(new_users) if new_users else None
                        )
                        maps_created += 1
                    except:
                        pass
                self.stdout.write(f'✅ Created {maps_created} RFID‑Jewellery mappings')
            else:
                self.stdout.write('⚠️ Cannot create maps: jewellery or RFID missing')
        else:
            self.stdout.write('✅ RFID‑Jewellery mappings already exist')

        self.stdout.write(self.style.SUCCESS('🎉 Data seeding completed!'))