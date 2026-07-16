import os
from datetime import date

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Exercise

# Create instances of Exercise
exercise1 = Exercise.objects.create(
    name="Push-ups",
    category="Strength",
    difficulty_level=4,
    duration_minutes=10,
    repetitions=50,
)

exercise2 = Exercise.objects.create(
    name="Running",
    category="Cardio",
    difficulty_level=7,
    duration_minutes=20,
    repetitions=0,
)

exercise3 = Exercise.objects.create(
    name="Pull-ups",
    category="Strength",
    difficulty_level=13,
    duration_minutes=35,
    repetitions=20,
)

# Print the results
long_and_hard_exercises = Exercise.get_long_and_hard_exercises()
print("Long and hard exercises:")
for exercise in long_and_hard_exercises:
    print('- ' + exercise.name)

short_and_easy_exercises = Exercise.get_short_and_easy_exercises()
print("Short and easy exercises:")
for exercise in short_and_easy_exercises:
    print('- ' + exercise.name)

exercises_within_duration = Exercise.get_exercises_within_duration(20, 40)
print(f"Exercises within 20 - 40 minutes:")
for exercise in exercises_within_duration:
    print('- ' + exercise.name)

exercises_with_difficulty_and_repetitions = Exercise.get_exercises_with_difficulty_and_repetitions(6, 15)
print(f"Exercises with difficulty 6+ and repetitions 15+:")
for exercise in exercises_with_difficulty_and_repetitions:
    print('- ' + exercise.name)