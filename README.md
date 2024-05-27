# Recipe Sharing Platform

This project is a recipe sharing platform built using Flask framework for REST APIs.

## Features

1. **User Authentication:** Users can sign up, log in, and manage their recipes securely.
2. **CRUD Operations:** Users can Create, Read, Update, and Delete recipes they own.
3. **Recipe Details:** Each recipe includes fields such as title, description, ingredients, preparation steps, cooking time, and serving size.
4. **Recipe Categories:** Users can categorize recipes into different categories (e.g., starter, main courses, desserts).
5. **Search and Filter:** Functionality is provided to search and filter recipes based on various criteria (e.g., category, ingredients, cooking time).
6. **Rating and Reviews:** Users can rate and review recipes, and the platform displays average ratings for each recipe.

## Endpoints

- `POST /register`: Register a new user.
- `POST /login`: Log in an existing user.
- `GET /recipes`: Get recipes owned by the authenticated user.
- Additional endpoints for CRUD operations, search, filter, rating, and reviews can be added.

## Dependencies

- Refer requirement.txt
## Setup

1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the Flask app using `python app.py`.

