import random
import lipsum

from yummyshare.db import db, Recipe, User, CUISINES, COURSES


def create_test_data():
    cuisines = [cui[0] for cui in CUISINES]
    courses = [cou[0] for cou in COURSES]
    file_names = ['breakfast.jpg', 'broccoli.jpg', 'chicken.jpg',
                  'pancakes.jpg', 'pizza.jpg', 'salad.jpg',
                  'salmon.jpg', 'salmon-1.jpg', 'shrimp.jpg', 'tarte.jpg']

    for i in range(100):
        recipe = Recipe(name=lipsum.generate_words(random.randint(1, 10)),
                        ingredients=lipsum.generate_sentences(2),
                        instructions=lipsum.generate_paragraphs(2),
                        cuisine=cuisines[random.randint(0, 4)],
                        course=courses[random.randint(0, 16)],
                        description=lipsum.generate_words(
                            random.randint(10, 20)),
                        image=file_names[random.randint(0, 9)],
                        user_id=random.randint(1, 5)
                        )
        # add recipe to the database
        db.session.add(recipe)
        db.session.commit()
