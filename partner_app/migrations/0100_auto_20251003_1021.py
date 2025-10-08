from django.db import migrations

def move_users_to_new_app(apps, schema_editor):
    OldUser = apps.get_model('partner_app', 'User')
    NewUser = apps.get_model('users', 'User')
    
    # Получаем всех пользователей
    old_users = OldUser.objects.all()
    
    # Создаем список новых пользователей
    new_users = []
    for old_user in old_users:
        new_user = NewUser(
            id=old_user.id,
            password=old_user.password,
            last_login=old_user.last_login,
            is_superuser=old_user.is_superuser,
            username=old_user.username,
            first_name=old_user.first_name,
            last_name=old_user.last_name,
            email=old_user.email,
            is_staff=old_user.is_staff,
            is_active=old_user.is_active,
            date_joined=old_user.date_joined,
            middle_name=old_user.middle_name,
            user_type=old_user.user_type,
            phone=old_user.phone,
            description=old_user.description,
            email_notifications=old_user.email_notifications,
            is_blocked=old_user.is_blocked,
            blocking_reason=old_user.blocking_reason,
            block_until=old_user.block_until
        )
        new_users.append(new_user)
    
    # Массовое создание (быстрее для больших объемов данных)
    NewUser.objects.bulk_create(new_users, batch_size=1000)

def move_users_back(apps, schema_editor):
    # NewUser = apps.get_model('users', 'User')
    # OldUser = apps.get_model('partner_app', 'User')
    
    # new_users = NewUser.objects.all()
    # old_users = []
    
    # for new_user in new_users:
    #     old_user = OldUser(
    #         id=new_user.id,
    #         password=new_user.password,
    #         last_login=new_user.last_login,
    #         is_superuser=new_user.is_superuser,
    #         username=new_user.username,
    #         first_name=new_user.first_name,
    #         last_name=new_user.last_name,
    #         email=new_user.email,
    #         is_staff=new_user.is_staff,
    #         is_active=new_user.is_active,
    #         date_joined=new_user.date_joined,
    #         middle_name=new_user.middle_name,
    #         user_type=new_user.user_type,
    #         phone=new_user.phone,
    #         description=new_user.description,
    #         email_notifications=new_user.email_notifications,
    #         is_blocked=new_user.is_blocked,
    #         blocking_reason=new_user.blocking_reason,
    #         block_until=new_user.block_until
    #     )
    #     old_users.append(old_user)
    
    # OldUser.objects.bulk_create(old_users, batch_size=1000)
    pass 

class Migration(migrations.Migration):
    dependencies = [    
        ('partner_app', '0099_delete_userreview'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(move_users_to_new_app, move_users_back),
    ]