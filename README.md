## Project Title

Fullstack FastAPI + MongoDB + Admin Panel + Auth

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your local machine:

Python (3.6 or higher)
FastAPI
Uvicorn (for running the app)
MongoDB

### Installing

Clone the repository to your local machine:

```
git clone https://github.com/arkrwn/FullstakFastAPI.git
cd FullstakFastAPI
```

Install the required dependencies:

```
pip install -r requirements.txt
```

### Configuration

Create a .env file in the root directory of the project, and add the following environment variable for the session secret key:

```
MONGO_HOST=mongodb://localhost:27017
DB_NAME=FullstackFastAPI
CLIENT_SECRET=RANDOMSEKRETDOANGINIMAHTAPIKUDU32
```

### Running the Application

Now that everything is set up, you can run the application using Uvicorn. From the project directory, execute the following command:

```
python3 app.py
```

Open your web browser and navigate to http://localhost:8000 to access the application.

You need to access register page first to register user, first user always set as admin

### Database Setup

Ensure MongoDB is running on your machine. You can use a MongoDB GUI like MongoDB Compass to create a new database and collections as per your application schema.

### Testing

Run the tests to ensure everything is working as expected:

```
pytest
```

### Deployment

For deployment, you can choose a cloud service like AWS or Heroku. Ensure you update the .env file with your production database credentials and other configurations. Also, remove the --reload flag from the Uvicorn command when running in a production environment.

### Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for details.
