import argparse
import os
import random

import django
import argparse


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from datacenter.models import Chastisement, Commendation, Lesson, Mark, Schoolkid
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


pozitive_comment = [
'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!'                
                    ]


def fix_marks(student_name):
   schoolkid = Schoolkid.objects.get(full_name__contains=student_name)
   bad_marks = Mark.objects.filter(schoolkid=schoolkid,points__in=[2,3])
   for bad_mark in bad_marks:
       bad_mark.points = 5
       bad_mark.save()


def remove_chastisements(student_name):
    child = Schoolkid.objects.get(full_name__contains=student_name)
    chast_student = Chastisement.objects.filter(schoolkid=child)
    chast_student.delete()


def create_commendation(student_name, subject):
    schoolkid = Schoolkid.objects.get(full_name__contains=student_name)
    lessons = Lesson.objects.filter(group_letter=schoolkid.group_letter, year_of_study=schoolkid.year_of_study, subject__title=subject)
    lesson = lessons.order_by('date').first()
    text = random.choice(pozitive_comment)
    Commendation.objects.get_or_create(
        subject=lesson.subject, schoolkid=schoolkid, created=lesson.date,teacher=lesson.teacher, text=text
    )


def main():
    parser = argparse.ArgumentParser(description='помогает ученику')
    parser.add_argument('--name', type=str, help='введите имя ученика')
    parser.add_argument('--subject', type=str, help='введите учебный предмет')
    args = parser.parse_args()
    create_commendation(args.name,args.subject)
    remove_chastisements(args.name)
    fix_marks(args.name)
    

if __name__ == "__main__":
    main()