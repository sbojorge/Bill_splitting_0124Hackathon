# Generated by Django 3.2.23 on 2024-01-20 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20240119_0723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='trip',
            new_name='event',
        ),
        migrations.RemoveField(
            model_name='event',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='event',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date_lock',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_locked',
        ),
        migrations.RemoveField(
            model_name='event',
            name='left_to_pay',
        ),
        migrations.RemoveField(
            model_name='event',
            name='total_expenses',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='receipt',
        ),
        migrations.AlterField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]