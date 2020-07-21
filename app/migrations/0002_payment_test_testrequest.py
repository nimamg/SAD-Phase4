# Generated by Django 3.0.8 on 2020-07-20 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('is_successful', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='test_request', to='app.Appointment')),
                ('payment_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='test_request', to='app.Payment')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='app.LabTest')),
                ('test_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='app.TestRequest')),
            ],
        ),
    ]