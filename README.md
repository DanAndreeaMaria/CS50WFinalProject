# Wellnest

Wellnest is a web application useful for everyone who needs a bit of time to reflect on their lives, experiences and thoughts. This application is created in such way that you are able to journal multiple times a day, complete a daily check-in, analyze the data and the app returns soft suggestions that may help you feel better about yourself. Even if it’s about sleep, energy, stress or maybe time for quality connections with other people, this app keeps you updated on how the last days went and adds the data into simple charts, so you clearly see the evolution, stagnation or maybe regression giving gentle messages about states and suggestions on how you can improve a mood or maybe keep some healthy habits so you feel good.
    Wellnest app lets you complete a daily check-in quiz where you can find six questions about the mood, energy and stress level, sleep quality, social interactions and enjoyable activities, each one with five select options from where to choose. After you press the submit button, on the index page you will find the results of the today’s check-in with the levels you chose. The check-ins are saved into the database and only the today’s check-in is displayed. I included a notification button with a red flag with the number ‘1’ on it which reminds you to complete the daily check-in and this way, you are allowing the app to analyze the data smoothly if you enter every day. The notification stops displaying the flag after you completed the daily check-in.
    Another feature is the journaling, a little place where you can put your thoughts and answer two important questions, ‘How are you feeling?’ and ‘How was your day?’ but also you can type freely on the provided text area on whatever thoughts you want to include and reflect on. After saving the entry, a message displays on the home page that the entry was saved and disappears after 3 seconds. The journals have no limit per day, so you can express yourself as much as you want. The cards that hold the journal moments have the border color according on your mood, from red for bad days to bright green for the best days, this way you can visualize them better.
    The analysis page is the place where the action happens. Here you can find the ‘Weekly wellbeing overview’, based on the last days (the app needs at least 3 days of data to generate charts, data and suggestions) and here are calculated the averages for the mood, energy, stress, sleep, social interactions and activities. Next we have the chart for ‘Mood over the last 7 days’ where I included only the mood, energy and stress. Each state has its own color to make it easier to visualize and below, the weekly insights are based on this chart and helps interpreting the data in a human readable content. The mood trend is created by comparing the first value to the last added value so you can see if the mood has improved since, is stable or it is slightly declining.
    I created a separate chart only for the sleep quality because sleep is directly influencing the other behaviors and it deserves its own analysis.
    After analyzing and visualizing the data, we can now focus on the gentle suggestions. These are generated for weekly averages, as daily encouragements for today’s values and daily random encouragement messages. In the analysis view I included single suggestions and also arrays with multiple messages, so you won’t be welcomed every time with the same suggestions and same encouragements in the same order. I specifically added a soft and friendly language so you won’t feel them as a burden, but as a help for you!

## Distinctiveness and Complexity

I believe this application stands out because I thought about a lot of important details that a user needs to be aware of and also be conscious about for a better mental wellbeing. This is the reason I chose this name ‘Wellnest’ because I wanted to be a nest where you put your feelings and thoughts and at the end of the day, reflect on them, listen to the suggestions and celebrate the real joys of life. This project is distinct from the other course projects because it is not simply a CRUD application. While is stores the data, it also performs analytical processing on that data, including trend detection, weekly averages, conditional feedback generator and dynamic chart rendering.
    Wellnest includes custom logic for behavioral analysis such as comparing first and last values to detect improvements or regressions, converting numeral scores into human-readable qualitative labels and generating personalized feedback based on aggregated weekly metrics.
    Additionally, the project integrates user authentication, relational database modeling, time-based filtering and dynamic frontend visualizations, making it more complex than earlier projects that we’re primarily focused on form handling or simple database interactions.
    Last but not least, I included an ‘About‘ page where I described what the application is doing and a disclaimer that this app is not suitable for severe mental health issues.
    This is not a medical application, all the suggestions are as gentle as possible so the recommendations are just about simple healthy habits like sleeping, paying attention on what makes you happy or feel good, celebrating the joys of life or how important rest is.

## Project structure and file overview

`models.py`
    Defines the database schema using Django ORM.
    Contains the **Entry** and **DailyCheckIn** models that store user-submitted metrics such as mood, day quality, energy, stress, sleep, social interaction and activity levels. This file establishes relationships between users and their check-in data.

`views.py`
    Handles application logic and request processing and contains view functions responsible for the following:

 - Rendering templates
 - Managing user authentication (registration, login, logout)
 - Rendering the main index page where journal entries are displayed and daily check-in completion is validated
 - Creating new Entry objects
 - Creating new DailyCheckIn objects
 - Performing analytical processing in the analysis view, including:
 - Converting numerical values into qualitative labels
 - Detecting behavioral trends over time
 - Filtering and retrieving the last 7 days of check-in data
 - Preparing structured datasets for chart visualization
 - Calculating weekly averages
 - Generating encouragements and suggestions - Rendering the informational about page
    This file contains the core analytical logic of the application.

`templates\wellnest`
    Contains all HTML templates responsible for frontend rendering using Django’s templating engine.
    about.html – Informational page describing the application
    analysis.html – Displays weekly analytics, averages, trends and charts
    daily_checkin.html – Form for submitting daily check-in data
    index.html – Main dashboard displaying journal entries
    layout.html – Base template providing shared structure (navbar, layout, styling references)
    login.html – User login form
    new_entry.html – Form for creating new journal entries
    register.html – User register form
    Templates dynamically render user-specific data passed from the backend

`static\wellnest`
    Contains static assets used for styling and interactivity.
    favicon_io – Favicon images used for browser tab branding

`script.js`
    JavaScript logic for: - Navbar notification interactions - Displaying the ‘Journal saved successfully’ message - Dynamically modifying journal border styling

`styles.css` – Global stylesheet defining layout, typography, colors and overall UI design

`urls.py` – Maps URL routes to corresponding view functions.

`admin.py` – registers database models for Django’s admin interface.

## How to run the application

1. Clone the repository:
   [https://github.com/me50/DanAndreeaMaria.git]

2. Navigate to the project directory:
   cd web50/projects/2020/x/capstone

3. Apply database migrations:
   python manage.py migrate

4. Run the development server
   python manage.py runserver

5. Open your browser and go to:
   [http://127.0.0.1:8000/]
