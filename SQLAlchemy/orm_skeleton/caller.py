"""
1. pip install sqlalchemy
2. pip install alembic
3. pip install psycopg
4. Create DB
5. Create Base class
6. alembic init alembic
7. Update target_metadata
8. Configure DB url
9. Create engine
"""
from typing import List, Any, Sequence

from sqlalchemy import create_engine, update, delete, ScalarResult, Row, RowMapping, select
from sqlalchemy.orm import sessionmaker

from helpers import handle_session
from models import Recipe, Chef

engine = create_engine(f"postgresql+psycopg2://postgres:admin@localhost/sql_alchemy_demo")
Session = sessionmaker(bind=engine)
session = Session()


@handle_session(session)
def create_recipe(name: str, ingredients: str, instructions: str) -> None:
    recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions
    )

    session.add(recipe)


@handle_session(session)
def update_recipe_by_name(name: str, new_name: str,  new_ingredients: str, new_instructions: str) -> None:
    """
    UPDATE recipe
    SET
        name = new_name,
        ingredients=new_ingredients,
        instructions=new_instructions
    WHERE
        name = <name>;
    """

    session.execute(
        update(Recipe)
        .where(Recipe.name == name)
        .values(
            name=new_name,
            ingredients=new_ingredients,
            instructions=new_instructions
        )
    )

@handle_session(session)
def delete_recipe_by_name(name: str) -> None:
    """
    DELETE FROM recipe
    WHERE name = <name>;
    """
    session.execute(
        delete(Recipe).where(Recipe.name == name)
    )


@handle_session(session, autoclose=False)
def get_recipes_by_ingredient(ingredient_name: str) -> Sequence[Row[Any] | RowMapping | Any]:
    """
    SELECT * FROM recipe WHERE ingredient ILIKE '%ingredient_name%';
    """
    return session.scalars(
        select(Recipe).where(
            Recipe.ingredients.ilike(f"%{ingredient_name}%")
        )
    ).all()


@handle_session(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str) -> None:
    first_recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == first_recipe_name)
        .with_for_update()  # Locks the record until transaction is finished
    ).one()
    second_recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == second_recipe_name)
        .with_for_update()  # Locks the record until transaction is finished
    ).one()

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


@handle_session(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str) -> str:
    recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == recipe_name)
    ).one()  # Recipe(...)

    if recipe.chef:
        raise Exception(f"Recipe: {recipe_name} already has a related chef")

    chef = session.scalars(
        select(Chef)
        .where(Chef.name == chef_name)
    ).one()
    recipe.chef = chef

    return f"Related recipe {recipe_name} with chef {chef_name}"


@handle_session(session)
def get_recipes_with_chef() -> str:
    """
    SELECT
        recipe.name,
        chef.name,
    FROM
        recipe
    JOIN
        chef
    ON
        chef.id = recipe.chef_id;
    """

    """
    recipes = session.scalars(
        select(Recipe.name, Chef.name).join(Recipe.chef)
    ).all()

    return "\n".join(
        f"Recipe: {r.name} made by chef: {c.name}"
        for r, c in recipes
    )
    """
    recipes = session.execute(
        select(Recipe.name, Chef.name).join(Recipe.chef)
    ).all()  # [("Pancakes", "Uti"), (...)]

    return "\n".join(
        f"Recipe: {recipe_name} made by chef: {chef_name}"
        for recipe_name, chef_name in recipes
    )
