This project is a Flask-based web application that allows users to log in using Google OAuth and update currency exchange rates from the National Bank of Ukraine (NBU) into a Google Sheets document.

## Key Features:
- Google OAuth Integration: Users can log in using their Google accounts.
- Date-based Currency Rate Updates: Users can input a date range to fetch and update USD exchange rates from the NBU.
- Google Sheets Integration: The fetched data is automatically updated in a specified Google Sheets document.

## Setup:
- Add Google OAuth credentials and app secret key in the .env file
- Set up a Google Sheets document and service account for gspread, add service configuration file and rename it to service-account.json
- Build image from Dockerfile and run the app
