HBnB Evolution - Part 2 (API Implementation)
Project Overview
This repository contains the second phase of the HBnB Evolution project. In this stage, we transitioned from basic object modeling to a functional RESTful API using the Flask framework and Flask-RESTx.

The application follows a layered architecture to ensure a clear separation of concerns between the user interface (Presentation Layer), the business logic (Domain Layer), and data handling (Persistence Layer).

Features
Layered Architecture: Clear separation between API endpoints, business logic, and data storage.

Facade Pattern: A central coordinator manages communication between layers, simplifying the API logic.

CRUD Operations: Full support for Create, Read, Update, and Delete operations for:

Users: Management of user profiles and administrative status.

Places: Listing of accommodations with geographic coordinates and pricing.

Amenities: Management of features like WiFi, Parking, or Air Conditioning.

Reviews: User-submitted feedback and ratings (1-5) for specific places.

Validation: Strict business logic validation (e.g., email formats, latitude/longitude boundaries, and non-negative pricing).

Swagger Documentation: Automatic API documentation and interactive testing interface.

Technology Stack
Python 3.x

Flask: Web framework.

Flask-RESTx: Extension for building REST APIs with Swagger support.

Unittest: Python’s built-in unit testing framework.

Project Structure
Plaintext
hbnb/
├── app/
│   ├── api/v1/          # Presentation Layer (API Endpoints)
│   ├── models/          # Business Logic Layer (Entity Models)
│   ├── services/        # Facade Pattern implementation
│   └── persistence/     # In-memory storage logic
├── tests/               # Automated unit tests
├── run.py               # Application entry point
└── config.py            # Environment configurations
Getting Started
1. Installation
Clone the repository and install the dependencies:

Bash
pip install -r requirements.txt
2. Running the Application
Start the Flask development server:

Bash
python run.py
The API will be accessible at http://127.0.0.1:5000/api/v1/.

3. API Documentation
Once the server is running, you can access the interactive Swagger UI to explore and test the endpoints directly from your browser:

http://127.0.0.1:5000/api/v1/

Testing
To run the automated test suite and verify the validation logic:

Bash
python -m unittest discover tests