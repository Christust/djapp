# Generated by Django 5.0.6 on 2024-06-17 01:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Creation date')),
                ('modified_at', models.DateField(auto_now=True, verbose_name='Modification date')),
                ('deleted_at', models.DateField(blank=True, null=True, verbose_name='Deletion date')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Creation date')),
                ('modified_at', models.DateField(auto_now=True, verbose_name='Modification date')),
                ('deleted_at', models.DateField(blank=True, null=True, verbose_name='Deletion date')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.country')),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Creation date')),
                ('modified_at', models.DateField(auto_now=True, verbose_name='Modification date')),
                ('deleted_at', models.DateField(blank=True, null=True, verbose_name='Deletion date')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.state')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Creation date')),
                ('modified_at', models.DateField(auto_now=True, verbose_name='Modification date')),
                ('deleted_at', models.DateField(blank=True, null=True, verbose_name='Deletion date')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.country')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.state')),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
            },
        ),
    ]
