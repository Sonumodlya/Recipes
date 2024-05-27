-- User table
CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Recipe table
CREATE TABLE Recipe (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    preparation_steps TEXT NOT NULL,
    cooking_time INTEGER NOT NULL,
    serving_size INTEGER NOT NULL,
    category_id INTEGER,
    user_id INTEGER
);

-- Recipe Category table
CREATE TABLE RecipeCategory (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Rating table
CREATE TABLE Rating (
    id INTEGER PRIMARY KEY,
    rating INTEGER NOT NULL,
    review TEXT,
    recipe_id INTEGER,
    user_id INTEGER
);


