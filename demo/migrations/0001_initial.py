# Generated by Django 2.1.10 on 2020-04-24 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='to_csv2',
            fields=[
                ('EMP_NO', models.TextField(blank=True, db_column='EMP_NO', primary_key=True, serialize=False)),
                ('JOB_SITUATION1', models.TextField(blank=True, db_column='JOB_SITUATION1', null=True)),
                ('JOB_SITUATION', models.BigIntegerField(blank=True, db_column='JOB_SITUATION', null=True)),
                ('NAME', models.TextField(blank=True, db_column='NAME', null=True)),
                ('SEX1', models.TextField(blank=True, db_column='SEX1', null=True)),
                ('SEX', models.BigIntegerField(blank=True, db_column='SEX', null=True)),
                ('BIRTH_DATE', models.TextField(blank=True, db_column='BIRTH_DATE', null=True)),
                ('AGE', models.BigIntegerField(blank=True, db_column='AGE', null=True)),
                ('IN_CONPANY_DATE', models.TextField(blank=True, db_column='IN_CONPANY_DATE', null=True)),
                ('HIRE_YEAR', models.FloatField(blank=True, db_column='HIRE_YEAR', null=True)),
                ('CLASS_START_DAY', models.TextField(blank=True, db_column='CLASS_START_DAY', null=True)),
                ('CLASS_YEAR', models.TextField(blank=True, db_column='CLASS_YEAR', null=True)),
                ('CURRENT_GRADE1', models.TextField(blank=True, db_column='CURRENT_GRADE1', null=True)),
                ('CURRENT_GRADE', models.FloatField(blank=True, db_column='CURRENT_GRADE', null=True)),
                ('CURRENT_GRADE_1', models.FloatField(blank=True, db_column='CURRENT_GRADE_1', null=True)),
                ('CURRENT_GRADE_2', models.FloatField(blank=True, db_column='CURRENT_GRADE_2', null=True)),
                ('CURRENT_GRADE_3', models.FloatField(blank=True, db_column='CURRENT_GRADE_3', null=True)),
                ('CURRENT_GRADE_4', models.FloatField(blank=True, db_column='CURRENT_GRADE_4', null=True)),
                ('CLASS1', models.TextField(blank=True, db_column='CLASS1', null=True)),
                ('CLASS_RANK', models.BigIntegerField(blank=True, db_column='CLASS_RANK', null=True)),
                ('CLASS_1', models.BigIntegerField(blank=True, db_column='CLASS_1', null=True)),
                ('CLASS_2', models.BigIntegerField(blank=True, db_column='CLASS_2', null=True)),
                ('CLASS_3', models.BigIntegerField(blank=True, db_column='CLASS_3', null=True)),
                ('CLASS_4', models.BigIntegerField(blank=True, db_column='CLASS_4', null=True)),
                ('CLASS_5', models.BigIntegerField(blank=True, db_column='CLASS_5', null=True)),
                ('CLASS_6', models.BigIntegerField(blank=True, db_column='CLASS_6', null=True)),
                ('CLASS_7', models.BigIntegerField(blank=True, db_column='CLASS_7', null=True)),
                ('CLASS_8', models.BigIntegerField(blank=True, db_column='CLASS_8', null=True)),
                ('CLASS_9', models.BigIntegerField(blank=True, db_column='CLASS_9', null=True)),
                ('CLASS_10', models.BigIntegerField(blank=True, db_column='CLASS_10', null=True)),
                ('CLASS_11', models.BigIntegerField(blank=True, db_column='CLASS_11', null=True)),
                ('CLASS_12', models.BigIntegerField(blank=True, db_column='CLASS_12', null=True)),
                ('CLASS_13', models.BigIntegerField(blank=True, db_column='CLASS_13', null=True)),
                ('CLASS_14', models.BigIntegerField(blank=True, db_column='CLASS_14', null=True)),
                ('CLASS_15', models.BigIntegerField(blank=True, db_column='CLASS_15', null=True)),
                ('CLASS_16', models.BigIntegerField(blank=True, db_column='CLASS_16', null=True)),
                ('CLASS_17', models.BigIntegerField(blank=True, db_column='CLASS_17', null=True)),
                ('CLASS_18', models.BigIntegerField(blank=True, db_column='CLASS_18', null=True)),
                ('CLASS_19', models.BigIntegerField(blank=True, db_column='CLASS_19', null=True)),
                ('CLASS_20', models.BigIntegerField(blank=True, db_column='CLASS_20', null=True)),
                ('WAGE', models.FloatField(blank=True, db_column='WAGE', null=True)),
                ('EDUCATION_NAME1', models.TextField(blank=True, db_column='EDUCATION_NAME1', null=True)),
                ('EDUCATION_NAME', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME', null=True)),
                ('EDUCATION_NAME_1', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME_1', null=True)),
                ('EDUCATION_NAME_2', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME_2', null=True)),
                ('EDUCATION_NAME_3', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME_3', null=True)),
                ('EDUCATION_NAME_4', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME_4', null=True)),
                ('EDUCATION_NAME_5', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME_5', null=True)),
                ('EDUCATION_NAME_6', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME_6', null=True)),
                ('EDUCATION_NAME_7', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME_7', null=True)),
                ('EDUCATION_NAME_8', models.BigIntegerField(blank=True, db_column='EDUCATION_NAME_8', null=True)),
                ('GRADUATE_SCHOOL', models.TextField(blank=True, db_column='GRADUATE_SCHOOL', null=True)),
                ('GRADUATE_SPECIALTY', models.TextField(blank=True, db_column='GRADUATE_SPECIALTY', null=True)),
                ('MARRIED1', models.TextField(blank=True, db_column='MARRIED1', null=True)),
                ('MARRIED', models.FloatField(blank=True, db_column='MARRIED', null=True)),
                ('MARRIED_1', models.FloatField(blank=True, db_column='MARRIED_1', null=True)),
                ('MARRIED_2', models.FloatField(blank=True, db_column='MARRIED_2', null=True)),
                ('JWH', models.TextField(blank=True, db_column='JWH', null=True)),
                ('JOB_TYPE1', models.TextField(blank=True, db_column='JOB_TYPE1', null=True)),
                ('JOB_TYPE', models.BigIntegerField(blank=True, db_column='JOB_TYPE', null=True)),
                ('JOB_TYPE_1', models.BigIntegerField(blank=True, db_column='JOB_TYPE_1', null=True)),
                ('JOB_TYPE_2', models.BigIntegerField(blank=True, db_column='JOB_TYPE_2', null=True)),
                ('JOB_TYPE_3', models.BigIntegerField(blank=True, db_column='JOB_TYPE_3', null=True)),
                ('JOB_TYPE_4', models.BigIntegerField(blank=True, db_column='JOB_TYPE_4', null=True)),
                ('JOB_TYPE_5', models.BigIntegerField(blank=True, db_column='JOB_TYPE_5', null=True)),
                ('JOB_TYPE_6', models.BigIntegerField(blank=True, db_column='JOB_TYPE_6', null=True)),
                ('JOB_TYPE_7', models.BigIntegerField(blank=True, db_column='JOB_TYPE_7', null=True)),
                ('JOB_TYPE_8', models.BigIntegerField(blank=True, db_column='JOB_TYPE_8', null=True)),
                ('JOB_TYPE_9', models.BigIntegerField(blank=True, db_column='JOB_TYPE_9', null=True)),
                ('JOB_TYPE_10', models.BigIntegerField(blank=True, db_column='JOB_TYPE_10', null=True)),
                ('JOB_TYPE_11', models.BigIntegerField(blank=True, db_column='JOB_TYPE_11', null=True)),
                ('JOB_TYPE_12', models.BigIntegerField(blank=True, db_column='JOB_TYPE_12', null=True)),
                ('JOB_TYPE_13', models.BigIntegerField(blank=True, db_column='JOB_TYPE_13', null=True)),
                ('PROVINCE_NAME', models.TextField(blank=True, db_column='PROVINCE_NAME', null=True)),
                ('PROVINCE_DISTANCE_RANK', models.FloatField(blank=True, db_column='PROVINCE_DISTANCE_RANK', null=True)),
                ('HOUSEHOLD1', models.TextField(blank=True, db_column='HOUSEHOLD1', null=True)),
                ('HOUSEHOLD_DISTANCE_RANK', models.FloatField(blank=True, db_column='HOUSEHOLD_DISTANCE_RANK', null=True)),
                ('HOUSEHOLD_h', models.TextField(blank=True, db_column='HOUSEHOLD_H', null=True)),
                ('HOUSEHOLD_1', models.FloatField(blank=True, db_column='HOUSEHOLD_1', null=True)),
                ('HOUSEHOLD_2', models.FloatField(blank=True, db_column='HOUSEHOLD_2', null=True)),
                ('HOUSEHOLD_3', models.FloatField(blank=True, db_column='HOUSEHOLD_3', null=True)),
                ('HOUSEHOLD_4', models.FloatField(blank=True, db_column='HOUSEHOLD_4', null=True)),
                ('HOUSEHOLD_5', models.FloatField(blank=True, db_column='HOUSEHOLD_5', null=True)),
                ('HOUSEHOLD_6', models.FloatField(blank=True, db_column='HOUSEHOLD_6', null=True)),
                ('HOUSEHOLD_7', models.FloatField(blank=True, db_column='HOUSEHOLD_7', null=True)),
                ('HOUSEHOLD_8', models.FloatField(blank=True, db_column='HOUSEHOLD_8', null=True)),
                ('HOUSEHOLD_9', models.FloatField(blank=True, db_column='HOUSEHOLD_9', null=True)),
                ('HOUSEHOLD_10', models.FloatField(blank=True, db_column='HOUSEHOLD_10', null=True)),
                ('HOUSEHOLD_11', models.FloatField(blank=True, db_column='HOUSEHOLD_11', null=True)),
                ('HOUSEHOLD_12', models.FloatField(blank=True, db_column='HOUSEHOLD_12', null=True)),
                ('HOUSEHOLD_13', models.FloatField(blank=True, db_column='HOUSEHOLD_13', null=True)),
                ('HOUSEHOLD_14', models.FloatField(blank=True, db_column='HOUSEHOLD_14', null=True)),
                ('HOUSEHOLD_15', models.FloatField(blank=True, db_column='HOUSEHOLD_15', null=True)),
                ('HOUSEHOLD_16', models.FloatField(blank=True, db_column='HOUSEHOLD_16', null=True)),
                ('HOUSEHOLD_17', models.FloatField(blank=True, db_column='HOUSEHOLD_17', null=True)),
                ('HOUSEHOLD_18', models.FloatField(blank=True, db_column='HOUSEHOLD_18', null=True)),
                ('HOUSEHOLD_19', models.FloatField(blank=True, db_column='HOUSEHOLD_19', null=True)),
                ('HOUSEHOLD_20', models.FloatField(blank=True, db_column='HOUSEHOLD_20', null=True)),
                ('HOUSEHOLD_21', models.FloatField(blank=True, db_column='HOUSEHOLD_21', null=True)),
                ('HOUSEHOLD_22', models.FloatField(blank=True, db_column='HOUSEHOLD_22', null=True)),
                ('HOUSEHOLD_23', models.FloatField(blank=True, db_column='HOUSEHOLD_23', null=True)),
                ('HOUSEHOLD_24', models.FloatField(blank=True, db_column='HOUSEHOLD_24', null=True)),
                ('HOUSEHOLD_25', models.FloatField(blank=True, db_column='HOUSEHOLD_25', null=True)),
                ('HOUSEHOLD_26', models.FloatField(blank=True, db_column='HOUSEHOLD_26', null=True)),
                ('HOUSEHOLD_27', models.FloatField(blank=True, db_column='HOUSEHOLD_27', null=True)),
                ('HOUSEHOLD_28', models.FloatField(blank=True, db_column='HOUSEHOLD_28', null=True)),
                ('HOUSEHOLD_29', models.FloatField(blank=True, db_column='HOUSEHOLD_29', null=True)),
                ('HOUSEHOLD_30', models.FloatField(blank=True, db_column='HOUSEHOLD_30', null=True)),
                ('HOUSEHOLD_31', models.FloatField(blank=True, db_column='HOUSEHOLD_31', null=True)),
                ('HIRE_TYPE_NAME1', models.TextField(blank=True, db_column='HIRE_TYPE_NAME1', null=True)),
                ('HIRE_TYPE_NAME', models.BigIntegerField(blank=True, db_column='HIRE_TYPE_NAME', null=True)),
                ('HIRE_TYPENAME_1', models.BigIntegerField(blank=True, db_column='HIRE_TYPENAME_1', null=True)),
                ('HIRE_TYPENAME_2', models.BigIntegerField(blank=True, db_column='HIRE_TYPENAME_2', null=True)),
                ('WORKTIME', models.TextField(blank=True, db_column='WORKTIME', null=True)),
                ('OT_TIME', models.TextField(blank=True, db_column='OT_TIME', null=True)),
                ('BUSINESSTRIP_DAY', models.TextField(blank=True, db_column='BUSINESSTRIP_DAY', null=True)),
                ('OFFICIALLEAVE_DAY', models.TextField(blank=True, db_column='OFFICIALLEAVE_DAY', null=True)),
                ('LATEEXCUSED_DAY', models.TextField(blank=True, db_column='LATEEXCUSED_DAY', null=True)),
                ('ABSENT_DAY', models.TextField(blank=True, db_column='ABSENT_DAY', null=True)),
                ('DIMISSION_YEAR1', models.TextField(blank=True, db_column='DIMISSION_YEAR1', null=True)),
                ('DIMISSION_YEAR', models.TextField(blank=True, db_column='DIMISSION_YEAR', null=True)),
                ('ISNEW1', models.TextField(blank=True, db_column='ISNEW1', null=True)),
                ('ISNEW', models.BigIntegerField(blank=True, db_column='ISNEW', null=True)),
                ('IS_GJRC1', models.TextField(blank=True, db_column='IS_GJRC1', null=True)),
                ('IS_GJRC', models.FloatField(blank=True, db_column='IS_GJRC', null=True)),
                ('MANAGESYSTEM', models.TextField(blank=True, db_column='MANAGESYSTEM', null=True)),
                ('DIMISSION_DATE', models.TextField(blank=True, db_column='DIMISSION_DATE', null=True)),
                ('IS_COMPLETED', models.TextField(blank=True, db_column='IS_COMPLETED', null=True)),
                ('DIMISSION_REASON_NAME', models.TextField(blank=True, db_column='DIMISSION_REASON_NAME', null=True)),
                ('DIMISSION_TYPE_NAME', models.TextField(blank=True, db_column='DIMISSION_TYPE_NAME', null=True)),
                ('PRED_LEAVE', models.TextField(blank=True, db_column='PRED_LEAVE', null=True)),
                ('SUB_BG_NAME', models.TextField(blank=True, db_column='SUB_BG_NAME', null=True)),
                ('COL_BU_NAME', models.TextField(blank=True, db_column='COL_BU_NAME', null=True)),
                ('JOB_NAME', models.TextField(blank=True, db_column='JOB_NAME', null=True)),
            ],
            options={
                'db_table': 'to_sql2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ToSql2',
            fields=[
                ('EMP_NO', models.TextField(blank=True, db_column='EMP_NO', primary_key=True, serialize=False)),
                ('JOB_SITUATION1', models.TextField(blank=True, db_column='JOB_SITUATION1', null=True)),
                ('JOB_SITUATION', models.IntegerField(blank=True, db_column='JOB_SITUATION', null=True)),
                ('NAME', models.TextField(blank=True, db_column='NAME', null=True)),
                ('SEX1', models.TextField(blank=True, db_column='SEX1', null=True)),
                ('SEX', models.IntegerField(blank=True, db_column='SEX', null=True)),
                ('BIRTH_DATE', models.TextField(blank=True, db_column='BIRTH_DATE', null=True)),
                ('AGE', models.IntegerField(blank=True, db_column='AGE', null=True)),
                ('IN_CONPANY_DATE', models.TextField(blank=True, db_column='IN_CONPANY_DATE', null=True)),
                ('HIRE_YEAR', models.FloatField(blank=True, db_column='HIRE_YEAR', null=True)),
                ('CLASS_START_DAY', models.TextField(blank=True, db_column='CLASS_START_DAY', null=True)),
                ('CLASS_YEAR', models.TextField(blank=True, db_column='CLASS_YEAR', null=True)),
                ('CURRENT_GRADE1', models.TextField(blank=True, db_column='CURRENT_GRADE1', null=True)),
                ('CURRENT_GRADE', models.FloatField(blank=True, db_column='CURRENT_GRADE', null=True)),
                ('CURRENT_GRADE_1', models.FloatField(blank=True, db_column='CURRENT_GRADE_1', null=True)),
                ('CURRENT_GRADE_2', models.FloatField(blank=True, db_column='CURRENT_GRADE_2', null=True)),
                ('CURRENT_GRADE_3', models.FloatField(blank=True, db_column='CURRENT_GRADE_3', null=True)),
                ('CURRENT_GRADE_4', models.FloatField(blank=True, db_column='CURRENT_GRADE_4', null=True)),
                ('CLASS1', models.TextField(blank=True, db_column='CLASS1', null=True)),
                ('CLASS_RANK', models.IntegerField(blank=True, db_column='CLASS_RANK', null=True)),
                ('CLASS_1', models.IntegerField(blank=True, db_column='CLASS_1', null=True)),
                ('CLASS_2', models.IntegerField(blank=True, db_column='CLASS_2', null=True)),
                ('CLASS_3', models.IntegerField(blank=True, db_column='CLASS_3', null=True)),
                ('CLASS_4', models.IntegerField(blank=True, db_column='CLASS_4', null=True)),
                ('CLASS_5', models.IntegerField(blank=True, db_column='CLASS_5', null=True)),
                ('CLASS_6', models.IntegerField(blank=True, db_column='CLASS_6', null=True)),
                ('CLASS_7', models.IntegerField(blank=True, db_column='CLASS_7', null=True)),
                ('CLASS_8', models.IntegerField(blank=True, db_column='CLASS_8', null=True)),
                ('CLASS_9', models.IntegerField(blank=True, db_column='CLASS_9', null=True)),
                ('CLASS_10', models.IntegerField(blank=True, db_column='CLASS_10', null=True)),
                ('CLASS_11', models.IntegerField(blank=True, db_column='CLASS_11', null=True)),
                ('CLASS_12', models.IntegerField(blank=True, db_column='CLASS_12', null=True)),
                ('CLASS_13', models.IntegerField(blank=True, db_column='CLASS_13', null=True)),
                ('CLASS_14', models.IntegerField(blank=True, db_column='CLASS_14', null=True)),
                ('CLASS_15', models.IntegerField(blank=True, db_column='CLASS_15', null=True)),
                ('CLASS_16', models.IntegerField(blank=True, db_column='CLASS_16', null=True)),
                ('CLASS_17', models.IntegerField(blank=True, db_column='CLASS_17', null=True)),
                ('CLASS_18', models.IntegerField(blank=True, db_column='CLASS_18', null=True)),
                ('CLASS_19', models.IntegerField(blank=True, db_column='CLASS_19', null=True)),
                ('CLASS_20', models.IntegerField(blank=True, db_column='CLASS_20', null=True)),
                ('WAGE', models.FloatField(blank=True, db_column='WAGE', null=True)),
                ('EDUCATION_NAME1', models.TextField(blank=True, db_column='EDUCATION_NAME1', null=True)),
                ('EDUCATION_NAME', models.IntegerField(blank=True, db_column='EDUCATION_NAME', null=True)),
                ('EDUCATION_NAME_1', models.IntegerField(blank=True, db_column='EDUCATION_NAME_1', null=True)),
                ('EDUCATION_NAME_2', models.IntegerField(blank=True, db_column='EDUCATION_NAME_2', null=True)),
                ('EDUCATION_NAME_3', models.IntegerField(blank=True, db_column='EDUCATION_NAME_3', null=True)),
                ('EDUCATION_NAME_4', models.IntegerField(blank=True, db_column='EDUCATION_NAME_4', null=True)),
                ('EDUCATION_NAME_5', models.IntegerField(blank=True, db_column='EDUCATION_NAME_5', null=True)),
                ('EDUCATION_NAME_6', models.IntegerField(blank=True, db_column='EDUCATION_NAME_6', null=True)),
                ('EDUCATION_NAME_7', models.IntegerField(blank=True, db_column='EDUCATION_NAME_7', null=True)),
                ('EDUCATION_NAME_8', models.IntegerField(blank=True, db_column='EDUCATION_NAME_8', null=True)),
                ('GRADUATE_SCHOOL', models.TextField(blank=True, db_column='GRADUATE_SCHOOL', null=True)),
                ('GRADUATE_SPECIALTY', models.TextField(blank=True, db_column='GRADUATE_SPECIALTY', null=True)),
                ('MARRIED1', models.TextField(blank=True, db_column='MARRIED1', null=True)),
                ('MARRIED', models.FloatField(blank=True, db_column='MARRIED', null=True)),
                ('MARRIED_1', models.FloatField(blank=True, db_column='MARRIED_1', null=True)),
                ('MARRIED_2', models.FloatField(blank=True, db_column='MARRIED_2', null=True)),
                ('JWH', models.TextField(blank=True, db_column='JWH', null=True)),
                ('JOB_TYPE1', models.TextField(blank=True, db_column='JOB_TYPE1', null=True)),
                ('JOB_TYPE', models.IntegerField(blank=True, db_column='JOB_TYPE', null=True)),
                ('JOB_TYPE_1', models.IntegerField(blank=True, db_column='JOB_TYPE_1', null=True)),
                ('JOB_TYPE_2', models.IntegerField(blank=True, db_column='JOB_TYPE_2', null=True)),
                ('JOB_TYPE_3', models.IntegerField(blank=True, db_column='JOB_TYPE_3', null=True)),
                ('JOB_TYPE_4', models.IntegerField(blank=True, db_column='JOB_TYPE_4', null=True)),
                ('JOB_TYPE_5', models.IntegerField(blank=True, db_column='JOB_TYPE_5', null=True)),
                ('JOB_TYPE_6', models.IntegerField(blank=True, db_column='JOB_TYPE_6', null=True)),
                ('JOB_TYPE_7', models.IntegerField(blank=True, db_column='JOB_TYPE_7', null=True)),
                ('JOB_TYPE_8', models.IntegerField(blank=True, db_column='JOB_TYPE_8', null=True)),
                ('JOB_TYPE_9', models.IntegerField(blank=True, db_column='JOB_TYPE_9', null=True)),
                ('JOB_TYPE_10', models.IntegerField(blank=True, db_column='JOB_TYPE_10', null=True)),
                ('JOB_TYPE_11', models.IntegerField(blank=True, db_column='JOB_TYPE_11', null=True)),
                ('JOB_TYPE_12', models.IntegerField(blank=True, db_column='JOB_TYPE_12', null=True)),
                ('JOB_TYPE_13', models.IntegerField(blank=True, db_column='JOB_TYPE_13', null=True)),
                ('PROVINCE_NAME', models.TextField(blank=True, db_column='PROVINCE_NAME', null=True)),
                ('PROVINCE_DISTANCE_RANK', models.FloatField(blank=True, db_column='PROVINCE_DISTANCE_RANK', null=True)),
                ('HOUSEHOLD1', models.TextField(blank=True, db_column='HOUSEHOLD1', null=True)),
                ('HOUSEHOLD_DISTANCE_RANK', models.FloatField(blank=True, db_column='HOUSEHOLD_DISTANCE_RANK', null=True)),
                ('HOUSEHOLD_h', models.TextField(blank=True, db_column='HOUSEHOLD_H', null=True)),
                ('HOUSEHOLD_1', models.FloatField(blank=True, db_column='HOUSEHOLD_1', null=True)),
                ('HOUSEHOLD_2', models.FloatField(blank=True, db_column='HOUSEHOLD_2', null=True)),
                ('HOUSEHOLD_3', models.FloatField(blank=True, db_column='HOUSEHOLD_3', null=True)),
                ('HOUSEHOLD_4', models.FloatField(blank=True, db_column='HOUSEHOLD_4', null=True)),
                ('HOUSEHOLD_5', models.FloatField(blank=True, db_column='HOUSEHOLD_5', null=True)),
                ('HOUSEHOLD_6', models.FloatField(blank=True, db_column='HOUSEHOLD_6', null=True)),
                ('HOUSEHOLD_7', models.FloatField(blank=True, db_column='HOUSEHOLD_7', null=True)),
                ('HOUSEHOLD_8', models.FloatField(blank=True, db_column='HOUSEHOLD_8', null=True)),
                ('HOUSEHOLD_9', models.FloatField(blank=True, db_column='HOUSEHOLD_9', null=True)),
                ('HOUSEHOLD_10', models.FloatField(blank=True, db_column='HOUSEHOLD_10', null=True)),
                ('HOUSEHOLD_11', models.FloatField(blank=True, db_column='HOUSEHOLD_11', null=True)),
                ('HOUSEHOLD_12', models.FloatField(blank=True, db_column='HOUSEHOLD_12', null=True)),
                ('HOUSEHOLD_13', models.FloatField(blank=True, db_column='HOUSEHOLD_13', null=True)),
                ('HOUSEHOLD_14', models.FloatField(blank=True, db_column='HOUSEHOLD_14', null=True)),
                ('HOUSEHOLD_15', models.FloatField(blank=True, db_column='HOUSEHOLD_15', null=True)),
                ('HOUSEHOLD_16', models.FloatField(blank=True, db_column='HOUSEHOLD_16', null=True)),
                ('HOUSEHOLD_17', models.FloatField(blank=True, db_column='HOUSEHOLD_17', null=True)),
                ('HOUSEHOLD_18', models.FloatField(blank=True, db_column='HOUSEHOLD_18', null=True)),
                ('HOUSEHOLD_19', models.FloatField(blank=True, db_column='HOUSEHOLD_19', null=True)),
                ('HOUSEHOLD_20', models.FloatField(blank=True, db_column='HOUSEHOLD_20', null=True)),
                ('HOUSEHOLD_21', models.FloatField(blank=True, db_column='HOUSEHOLD_21', null=True)),
                ('HOUSEHOLD_22', models.FloatField(blank=True, db_column='HOUSEHOLD_22', null=True)),
                ('HOUSEHOLD_23', models.FloatField(blank=True, db_column='HOUSEHOLD_23', null=True)),
                ('HOUSEHOLD_24', models.FloatField(blank=True, db_column='HOUSEHOLD_24', null=True)),
                ('HOUSEHOLD_25', models.FloatField(blank=True, db_column='HOUSEHOLD_25', null=True)),
                ('HOUSEHOLD_26', models.FloatField(blank=True, db_column='HOUSEHOLD_26', null=True)),
                ('HOUSEHOLD_27', models.FloatField(blank=True, db_column='HOUSEHOLD_27', null=True)),
                ('HOUSEHOLD_28', models.FloatField(blank=True, db_column='HOUSEHOLD_28', null=True)),
                ('HOUSEHOLD_29', models.FloatField(blank=True, db_column='HOUSEHOLD_29', null=True)),
                ('HOUSEHOLD_30', models.FloatField(blank=True, db_column='HOUSEHOLD_30', null=True)),
                ('HOUSEHOLD_31', models.FloatField(blank=True, db_column='HOUSEHOLD_31', null=True)),
                ('HIRE_TYPE_NAME1', models.TextField(blank=True, db_column='HIRE_TYPE_NAME1', null=True)),
                ('HIRE_TYPE_NAME', models.IntegerField(blank=True, db_column='HIRE_TYPE_NAME', null=True)),
                ('HIRE_TYPENAME_1', models.IntegerField(blank=True, db_column='HIRE_TYPENAME_1', null=True)),
                ('HIRE_TYPENAME_2', models.IntegerField(blank=True, db_column='HIRE_TYPENAME_2', null=True)),
                ('WORKTIME', models.TextField(blank=True, db_column='WORKTIME', null=True)),
                ('OT_TIME', models.TextField(blank=True, db_column='OT_TIME', null=True)),
                ('BUSINESSTRIP_DAY', models.TextField(blank=True, db_column='BUSINESSTRIP_DAY', null=True)),
                ('OFFICIALLEAVE_DAY', models.TextField(blank=True, db_column='OFFICIALLEAVE_DAY', null=True)),
                ('LATEEXCUSED_DAY', models.TextField(blank=True, db_column='LATEEXCUSED_DAY', null=True)),
                ('ABSENT_DAY', models.TextField(blank=True, db_column='ABSENT_DAY', null=True)),
                ('DIMISSION_YEAR1', models.TextField(blank=True, db_column='DIMISSION_YEAR1', null=True)),
                ('DIMISSION_YEAR', models.TextField(blank=True, db_column='DIMISSION_YEAR', null=True)),
                ('ISNEW1', models.TextField(blank=True, db_column='ISNEW1', null=True)),
                ('ISNEW', models.IntegerField(blank=True, db_column='ISNEW', null=True)),
                ('IS_GJRC1', models.TextField(blank=True, db_column='IS_GJRC1', null=True)),
                ('IS_GJRC', models.FloatField(blank=True, db_column='IS_GJRC', null=True)),
                ('MANAGESYSTEM', models.TextField(blank=True, db_column='MANAGESYSTEM', null=True)),
                ('DIMISSION_DATE', models.TextField(blank=True, db_column='DIMISSION_DATE', null=True)),
                ('IS_COMPLETED', models.TextField(blank=True, db_column='IS_COMPLETED', null=True)),
                ('DIMISSION_REASON_NAME', models.TextField(blank=True, db_column='DIMISSION_REASON_NAME', null=True)),
                ('DIMISSION_TYPE_NAME', models.TextField(blank=True, db_column='DIMISSION_TYPE_NAME', null=True)),
                ('PRED_LEAVE', models.TextField(blank=True, db_column='PRED_LEAVE', null=True)),
                ('SUB_BG_NAME', models.TextField(blank=True, db_column='SUB_BG_NAME', null=True)),
                ('COL_BU_NAME', models.TextField(blank=True, db_column='COL_BU_NAME', null=True)),
                ('JOB_NAME', models.TextField(blank=True, db_column='JOB_NAME', null=True)),
            ],
            options={
                'db_table': 'to_sql2',
                'managed': False,
            },
        ),
    ]
