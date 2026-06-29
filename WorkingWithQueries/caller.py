import os
from typing import List

import django
from django.db.models.sql import Query

from populate_db import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Case, When, Value, Q, F, QuerySet
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout
from main_app.choices import LaptopChoice, OSChoice

"""
SELECT * FROM artwork_gallery 
ORDER BY rating DESC, id ASC
LIMIT 1;
"""
def show_highest_rated_art() -> str:
    highest_rated_art = ArtworkGallery.objects.order_by(
        '-rating', 'id'
    ).first()

    return f"{highest_rated_art.art_name} is the highest-rated art with a {highest_rated_art.rating} rating!"


"""
INSERT INTO 
    artwork_gallery
VALUES 
    (...), 
    (...);
"""
def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create([
        first_art, second_art
    ])



"""
DELETE FROM artwork_gallery
WHERE rating < 0;
"""
def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop() -> str:
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()
    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


"""
UPDATE laptop
SET storage = 512
WHERE brand IN ('Asus', 'Lenovo');
"""
def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=[LaptopChoice.ASUS, LaptopChoice.LENOVO]).update(storage=512)


def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=[LaptopChoice.ACER, LaptopChoice.DELL, LaptopChoice.APPLE]).update(memory=16)


"""
-- Option 2
UPDATE laptop
SET os = ...
WHERE brand in [..., ...]; -- x4

-- Option 3
UPDATE laptop
SET os = CASE
    WHEN ... THEN ...
END 
"""
def update_operation_systems():
    # Solution 1: really bad
    # for laptop in Laptop.objects.all(): ...

    # Solution 2: okay
    # Laptop.objects.filter(brand=LaptopChoice.ASUS).update(operation_system=OSChoice.WINDOWS)
    # Laptop.objects.filter(brand=LaptopChoice.APPLE).update(operation_system=OSChoice.MACOS)
    # Laptop.objects.filter(brand__in=[LaptopChoice.ACER, LaptopChoice.DELL]).update(operation_system=OSChoice.LINUX)
    # Laptop.objects.filter(brand=LaptopChoice.LENOVO).update(operation_system=OSChoice.CHROME_OS)

    # Solution 3: best
    Laptop.objects.update(
        operation_system=Case(
            When(brand=LaptopChoice.ASUS, then=Value(OSChoice.WINDOWS)),
            When(brand=LaptopChoice.APPLE, then=Value(OSChoice.MACOS)),
            When(brand=LaptopChoice.LENOVO, then=Value(OSChoice.CHROME_OS)),
            When(brand__in=[LaptopChoice.ACER, LaptopChoice.DELL], then=Value(OSChoice.LINUX)),
        )
    )


def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()



def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title="no title").delete()


"""
UPDATE chess_player
SET games_won = 30
WHERE title = 'GM'
"""
def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title="GM").update(games_won=30)


def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title="no title").update(games_lost=25)


def change_chess_games_drawn() -> None:
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM() -> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


"""
UPDATE chess_player
SET title = 'IM'
WHERE rating BETWEEN 2300 AND 2399
"""
def grand_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title='IM')


def grand_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title='FM')


def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title='regular player')


def set_new_chefs() -> None:
    Meal.objects.update(
        chef=Case(
          When(meal_type="Breakfast", then=Value('Gordon Ramsay')),
          When(meal_type="Dinner", then=Value('Jamie Oliver')),
          When(meal_type="Lunch", then=Value('Julia Child')),
          When(meal_type="Snack", then=Value('Thomas Keller')),
        ),
    )


def set_new_preparation_times() -> None:
    Meal.objects.update(
        preparation_time=Case(
          When(meal_type="Breakfast", then=Value('10 minutes')),
          When(meal_type="Dinner", then=Value('15 minutes')),
          When(meal_type="Lunch", then=Value('12 minutes')),
          When(meal_type="Snack", then=Value('5 minutes')),
        ),
    )


def update_low_calorie_meals() -> None:
    # Option 1: SELECT * FROM meals WHERE meal_type = 'Breakfast' or meal_type = 'Dinner'
    # Meal.objects.filter(Q(meal_type="Breakfast") | Q(meal_type="Dinner"))

    Meal.objects.filter(meal_type__in=["Breakfast", "Dinner"]).update(calories=400)


def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=["Lunch", "Snack"]).update(calories=700)


def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=["Lunch", "Snack"]).delete()


def show_hard_dungeons() -> str:
    hard_dungeons = Dungeon.objects.filter(
        difficulty="Hard",
    ).order_by('-location')

    return '\n'.join(
        f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!"
        for d in hard_dungeons
    )


def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)


def update_dungeon_names() -> None:
    Dungeon.objects.update(
        name=Case(
            When(difficulty="Easy", then=Value("The Erased Thombs")),
            When(difficulty="Medium", then=Value("The Coral Labyrinth")),
            When(difficulty="Hard", then=Value("The Lost Haunt")),
            default=F('name')  # ELSE
        )
    )


"""
UPDATE dungeon
SET boss_health = 500
WHERE difficulty != 'Easy'
"""
def update_dungeon_bosses_health() -> None:
    Dungeon.objects.exclude(
        difficulty="Easy",
    ).update(boss_health=500)

    # Dungeon.objects.filter(
    #     difficulty__ne="Easy",
    # ).update(boss_health=500)


def update_dungeon_recommended_levels() -> None:
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty="Easy", then=Value(25)),
            When(difficulty="Medium", then=Value(50)),
            When(difficulty="Hard", then=Value(75)),
            default=F('recommended_level')  # ELSE
        )
    )


def set_new_locations() -> None:
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value("Enchanted Maze")),
            When(recommended_level=50, then=Value("Grimstone Mines")),
            When(recommended_level=75, then=Value("Shadowed Abyss")),
            default=F('location')  # ELSE
        )
    )

def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value("1000 Gold")),
            When(location__startswith="E", then=Value("New dungeon unlocked")),  # LIKE 'E%'
            When(location__endswith="s", then=Value("Dragonheart Amulet")),  # LIKE '%s'
            default=F('reward')  # ELSE
        )
    )


def show_workouts() -> str:
    workouts = Workout.objects.filter(
        workout_type__in=[
            "Calisthenics",
            "CrossFit",
        ]
    ).order_by('id')

    return '\n'.join(f"{w.name} from {w.workout_type} type has {w.difficulty} difficulty!" for w in workouts)


"""
WHERE difficulty = 'Hard' AND workout_type='Cardio'
"""
def get_high_difficulty_cardio_workouts() -> QuerySet[Workout]:
    return Workout.objects.filter(
        difficulty="High",
        workout_type="Cardio",
    ).order_by('instructor')

def set_new_instructors() -> None:
    Workout.objects.update(
        instructor=Case(
            When(workout_type="Cardio", then=Value("John Smith")),
            When(workout_type="Strength", then=Value("Michael Williams")),
            When(workout_type="Yoga", then=Value("Emily Johnson")),
            When(workout_type="CrossFit", then=Value("Sarah Davis")),
            When(workout_type="Calisthenics", then=Value("Chris Heria")),
            default=F('instructor')
        )
    )

def set_new_duration_times() -> None:
    Workout.objects.update(
        duration=Case(
            When(instructor="John Smith", then=Value("15 minutes")),
            When(instructor="Sarah Davis", then=Value("30 minutes")),
            When(instructor="Chris Heria", then=Value("45 minutes")),
            When(instructor="Michael Williams", then=Value("1 hour")),
            When(instructor="Emily Johnson", then=Value("1 hour and 30 minutes")),
            default=F('duration')
        )
    )


def delete_workouts() -> None:
    Workout.objects.exclude(workout_type__in=["Strength", "Calisthenics"]).delete()
