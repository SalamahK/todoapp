# Generated by Django 4.2.11 on 2024-05-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_category_created_alter_category_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='category',
        ),
        migrations.AddField(
            model_name='todolist',
            name='categories',
            field=models.ManyToManyField(to='todolist.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='created',
            field=models.DateField(default='2024-05-13'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateField(default='2024-05-13'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(default='2024-05-13'),
        ),
    ]
