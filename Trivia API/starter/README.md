# Full Stack API Final Project


## trivia API
This project is done to sharpen my skills in developing an API based web site.
It is about general knowedlge questions, where you can enjoy and play, and test your knwoedgle and share your results with friends and family!

## Getting started
### Installation 
in backend folder, you can see requirements.txt file, where you can install all needed libraries to run the website. simply -when you at backend directory- run:\
`
pip3 install -r requirements.txt
`\
to install frontend, you need to install node packet manager, and on frontend diretory, run:\
`
npm install
`
(after installation, you will see some vulnerabilities, you should then run `npm audit fix`, and you can ignore the rest of vulnerabilities after that run.)
### Linking Database
you can link your own database by making envoirment variables using these nams: \
`
DB_HOST
`
`
DB_USER
`
`
DB_PASSWORD
`
if any of these variables does not exist, a defualt value will be assigned, and they are:\
`
DB_HOST = '127.0.0.1:5432'
`
`
DB_USER = 'postgres'
`
`
DB_PASSWORD = 'postgres'
`
### Local Development
When working localy, IP should be 'localhost', and on backend directory, run the following (on Windows)\
`
$env:FLASK_APP="flaskr"
`
###  Running Application and Testing
To run the app. for the backend run: `flask run`, and `npm start` for the frontend.

# API Documenation

## Getting Started
* Base URL: This is an offline app, so it can only be run locally, on port 500. meaning, our base URL is  `localhost:5000`.
* Sending and receiveing data are ALL in json format. 
## Endpoints
### GET /api/categories
* Return a list of dicts of all existed categroies in the database.
* Example `curl http://127.0.0.1:5000/api/categories`\
\
`{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}`
### GET /api/questions
* Return a list of dicts of all existed categroies in the database.
* Example `curl http://127.0.0.1:5000/api/questions`\
\
`
"questions": [
    {
      "answer": "the office",
      "category": 2,
      "difficulty": 5,
      "id": 48,
      "question": "what is the BEST sitcom show?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
`
### GET /api/categories/<int:category_id>/questions
* Return a list of questions for a specific category.
* Example `curl http://127.0.0.1:5000/api/categories/2/questions`\
\
`
"questions": [
{
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "the office",
      "category": 2,
      "difficulty": 5,
      "id": 48,
      "question": "what is the BEST sitcom show?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "totalQuestions": 2
}
`
# Acknowledgemnt
I would like to thank my mentor Mashael for always support us, her students. I would also thank my colleagues Saud and Najla for helping me discovring few bugs.
