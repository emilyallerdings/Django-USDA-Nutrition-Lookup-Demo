## Description

A basic demo for a django web app which utilizes an external API from USDA for nutrition look-up and a local databse for user authentication.

Run using python manage.py runserver.

Only runs locally for now at http://127.0.0.1:8000/.

## Configuration

To run this project, you need to set up a `.env` file in the /foodsearch/ directory. This file should contain the following environment variables:

```dotenv
# Django secret key
SECRET_KEY=your_django_secret_key_here

# USDA API key
USDA_API_KEY=your_api_key_here
```

A USDA API key can be obtained for free [here]([URL](https://fdc.nal.usda.gov/api-key-signup.html))
