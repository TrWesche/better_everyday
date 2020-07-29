# Setup requirements
In order to get the environment running an environment file named .env will need to be created with the following parameters:
```
SECRET_KEY = 'secret_key'
FLASK_APP = 'wsgi.py'

SQLALCHEMY_DATABASE_URI_PROD = "prod_database_path"

SQLALCHEMY_DATABASE_URI_TEST = "test_database_path"
```

# The Database Schema will consist of 19 tables.

## User Tables:
- Auth - Table for user authentication
- Users - Table for PII

## Community Forum Tables:
- Community - Master record for an entire community
- Thread - Each community can have multiple threads
- Post - Each thread consists of multiple posts
- Community_Personas - Relationship table for linking multiple target personas to their relevant communities
- Community_Habits - Relationship table for linking multiple target habits to their relevant communities
- Community_Goals - Relationship table for linking multiple target goals to their relevant communities

## Habit Tables:
- Persona - List of User Personas
- Habit - List of User Habits
- Goals - List of User Goals
- User_Persona - Relationship table linking users to their target personas
- User_Habit - Relationship table linking users to their target habits, overarching personas, goal scoring system, and goal reminder schedule
- User_Goal - Relationship table linking users to their target goals, overarching personas, goal scoring system, and goal reminder schedule

## Tracking Tables:
- Goal_Score - List of scores and associated dates for user goals
- Habit_Score - List of scores and associated dates for user habits
- Scoring_System - Definition of scoring system used for the target goal
- Scoring_System_Params - Details on breakpoints and their meaning for the target goal
- Reminder_Schedule - Lookup for driving user reminders based on day of week & time


### The reference picture attached below includes 4 tables for messaging functionality which will not be included in v1 of the project.
![DB Schema](application/DB_Schema.png "Better Everyday Database Schema")


# API(s) Utilized

1. The main API targeted for utilization is the Google Charts API to allow for data visualization on the platform:
    - https://developers.google.com/chart

2. Additional API option - Pexels API for user site customization with images provided by the service:
   - https://www.pexels.com/api/documentation/ 

3. Additional API option - TheSaidSo API for serving "inspirational" quotes to platform users:
   - https://quotes.rest/

Note: For all external APIs which require validation a "key" file must be added to the api folder with a valid API key variable.