import os
import uuid

from flask import Blueprint, abort, render_template, redirect, request, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from yummyshare.db import db, Recipe
from .forms import RecipeForm, RecipeUpdateForm, CUISINES, COURSES


bp = Blueprint('recipe', __name__, url_prefix='/')


@bp.route('/')
def index():
    """
    Home Page.
    """
    recipes = Recipe.query.order_by(Recipe.created_datetime.desc()).limit(4)
    return render_template('recipe/index.html', recipes=recipes, courses=COURSES)


@bp.route('/recipe/create/', methods=['GET', 'POST'])
@login_required
def create():
    """
    Create recipe.
    """
    form = RecipeForm()
    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        new_filename = '{}.{}'.format(
            str(uuid.uuid4()),  filename.split('.')[-1])
        file_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)

        recipe = Recipe(name=form.name.data,
                        ingredients=form.ingredients.data,
                        instructions=form.instructions.data,
                        cuisine=form.cuisine.data,
                        course=form.course.data,
                        description=form.description.data,
                        image=new_filename,
                        user_id=current_user.id
                        )
        # add recipe to the database
        db.session.add(recipe)
        db.session.commit()

        flash(u'Recipe published successfully!', 'success')
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))

    return render_template('recipe/create.html', form=form)


def get_recipe(id):
    recipe = Recipe.query.filter_by(id=id).first()

    if recipe is None:
        abort(404, 'Recipe doest not exist.')

    return recipe


@bp.route('/recipe/<int:recipe_id>/')
def view_recipe(recipe_id):
    """
    View recipe.
    """
    recipe = get_recipe(recipe_id)
    return render_template('recipe/recipe.html', recipe=recipe)


@bp.route('/recipe/<int:recipe_id>/update/', methods=['GET', 'POST'])
@login_required
def update(recipe_id):
    """
    Update recipe.
    """
    form = RecipeUpdateForm()
    recipe = get_recipe(recipe_id)

    if recipe.user.id != current_user.id:
        abort(403, 'You are not authorized to do this action.')

    if form.validate_on_submit():

        new_filename = None
        if form.image.data:
            # remove old file first
            # os.remove(os.path.join(
            #     current_app.config['UPLOAD_FOLDER'], recipe.image))

            # store new one
            file = form.image.data
            filename = secure_filename(file.filename)
            new_filename = '{}.{}'.format(
                str(uuid.uuid4()),  filename.split('.')[-1])
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)

        Recipe.query.filter_by(id=recipe_id).update(
            dict(name=form.name.data,
                 ingredients=form.ingredients.data,
                 instructions=form.instructions.data,
                 cuisine=form.cuisine.data,
                 course=form.course.data,
                 description=form.description.data
                 )
        )
        if new_filename:
            Recipe.query.filter_by(id=recipe_id).update(
                dict(image=new_filename))
        db.session.commit()

        flash(u'Recipe updated successfully!', 'success')
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))

    return render_template('recipe/update.html', form=form, recipe=recipe, cuisines=CUISINES, courses=COURSES)


@bp.route('/recipe/<int:recipe_id>/delete/', methods=['POST'])
@login_required
def delete(recipe_id):
    """
    Delete recipe.
    """
    recipe = get_recipe(recipe_id)

    if recipe.user.id != current_user.id:
        abort(403, 'You are not authorized to do this action.')

    # remove image file
    # os.remove(os.path.join(
    #     current_app.config['UPLOAD_FOLDER'], recipe.image))

    db.session.delete(recipe)
    db.session.commit()

    flash(u'Recipe deleted!', 'danger')
    return redirect(url_for('recipe.index'))


@bp.route('/recipe/<int:recipe_id>/toggle-save/', methods=['POST'])
@login_required
def toggle_save(recipe_id):
    recipe = get_recipe(recipe_id)

    # user already saved the recipe, so unsave it
    if recipe in current_user.saved_recipes:
        current_user.saved_recipes.remove(recipe)
        flash(u'Recipe unsaved!', 'info')
    else:
        flash(u'Recipe saved!', 'success')
        current_user.saved_recipes.append(recipe)

    db.session.commit()
    return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))


@bp.route('/recipes/<string:course>/page/<int:page>/')
def browse(course, page):
    recipes = Recipe.query.filter_by(course=course).order_by(Recipe.created_datetime.desc()).paginate(
        per_page=9, page=page, error_out=True
    )

    title = ''
    for cou in COURSES:
        if cou[0] == course:
            title = cou[1]

    return render_template('recipe/browse.html', recipes=recipes, course=course, page=page, title=title)


@bp.route('/my-recipes/page/<int:page>/')
@login_required
def my_recipes(page):
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.created_datetime.desc()).paginate(
        per_page=9, page=page, error_out=True
    )

    title = 'My Recipes'

    return render_template('recipe/my_recipes.html', recipes=recipes, page=page, title=title)


@bp.route('/saved-recipes/page/<int:page>/')
@login_required
def saved_recipes(page):
    recipes = Recipe.query.join(Recipe.users).filter_by(id=current_user.id).order_by(Recipe.created_datetime.desc()).paginate(
        per_page=9, page=page, error_out=True
    )

    title = 'Saved Recipes'

    return render_template('recipe/saved_recipes.html', recipes=recipes, page=page, title=title)


@bp.route('/recipe/search/<int:page>/')
def search(page):
    search_term = request.args.get('q')
    keyword = "%{}%".format(search_term)
    recipes = Recipe.query.filter(Recipe.name.like(keyword)).order_by(Recipe.created_datetime.desc()).paginate(
        per_page=9, page=page, error_out=True
    )

    title = 'Search results for ' + search_term

    return render_template('recipe/search_results.html', recipes=recipes, page=page, title=title, search_term=search_term)
