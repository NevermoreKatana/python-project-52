# Generated by Django 4.2.6 on 2023-10-27 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_alter_labels_name'),
        ('tasks', '0002_alter_tasks_executor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, to='labels.labels'),
        ),
    ]
