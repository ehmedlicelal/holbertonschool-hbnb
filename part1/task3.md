# HBnB Technical Documentation

## 1. Introduction

This document provides a comprehensive technical overview of the HBnB application architecture and design. It serves as a blueprint for the development process by illustrating the system structure, core business logic, and interaction flows.

The document includes:
- High-Level Architecture (Package Diagram)
- Business Logic Layer (Class Diagram)
- API Interaction Flow (Sequence Diagrams)

The goal is to ensure clarity, maintainability, and scalability of the system.

---

## 2. High-Level Architecture

### Package Diagram

```mermaid
flowchart TD

subgraph Presentation_Layer
    UI[User Interface]
    API[API Controllers]
end

subgraph Business_Logic_Layer
    Facade[Facade]
    Services[Services]
    
    subgraph Models
        User
        Place
        Review
        Amenity
    end
end

subgraph Persistence_Layer
    Repositories[Repositories]
    Database[(Database)]
end

UI --> Facade
API --> Facade

Facade --> Services
Services --> User
Services --> Place
Services --> Review
Services --> Amenity

Services --> Repositories
Repositories --> Database
```

### Explanation

The system follows a **three-layer architecture**:

- **Presentation Layer**
  - Handles user interaction via UI and API
  - Sends requests to the system

- **Business Logic Layer**
  - Contains core application logic
  - Includes services, models, and a facade

- **Persistence Layer**
  - Manages database operations
  - Uses repositories for data access

### Facade Pattern

The **Facade** acts as a single entry point to the Business Logic Layer.  
It simplifies communication and reduces coupling between layers.

---

## 3. Business Logic Layer

### Class Diagram

```mermaid
classDiagram

class User {
    +UUID id
    +string first_name
    +string last_name
    +string email
    +string password
    +datetime created_at
    +datetime updated_at
    +create()
    +update()
    +delete()
}

class Place {
    +UUID id
    +string title
    +string description
    +float price
    +datetime created_at
    +datetime updated_at
    +create()
    +update()
    +delete()
}

class Review {
    +UUID id
    +string text
    +int rating
    +datetime created_at
    +datetime updated_at
    +create()
    +update()
    +delete()
}

class Amenity {
    +UUID id
    +string name
    +datetime created_at
    +datetime updated_at
    +create()
    +update()
    +delete()
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : has
Place "0..*" --> "0..*" Amenity : includes
Review --> User : author
Review --> Place : place
```

### Explanation

#### Entities

- **User**: Represents application users
- **Place**: Represents property listings
- **Review**: Represents feedback on places
- **Amenity**: Represents features (e.g., Wi-Fi, parking)

#### Design Decisions

- Each entity includes:
  - Unique identifier (UUID)
  - Creation and update timestamps
- CRUD methods are defined for basic operations

#### Relationships

- A User can own multiple Places
- A User can write multiple Reviews
- A Place can have multiple Reviews
- A Place can have multiple Amenities (many-to-many)
- A Review is linked to both User and Place

---

## 4. API Interaction Flow

### 4.1 User Registration

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant Service
participant Repository
participant Database

User->>API: POST /users
API->>Facade: create_user(data)
Facade->>Service: validate_user(data)
Service->>Repository: save_user(user)
Repository->>Database: INSERT user
Database-->>Repository: success
Repository-->>Service: user saved
Service-->>Facade: return user
Facade-->>API: response
API-->>User: 201 Created
```

---

### 4.2 Place Creation

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant Service
participant Repository
participant Database

User->>API: POST /places
API->>Facade: create_place(data)
Facade->>Service: validate_place(data)
Service->>Repository: save_place(place)
Repository->>Database: INSERT place
Database-->>Repository: success
Repository-->>Service: place saved
Service-->>Facade: return place
Facade-->>API: response
API-->>User: 201 Created
```

---

### 4.3 Review Submission

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant Service
participant Repository
participant Database

User->>API: POST /reviews
API->>Facade: create_review(data)
Facade->>Service: validate_review(data)
Service->>Repository: save_review(review)
Repository->>Database: INSERT review
Database-->>Repository: success
Repository-->>Service: review saved
Service-->>Facade: return review
Facade-->>API: response
API-->>User: 201 Created
```

---

### 4.4 Fetch List of Places

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant Service
participant Repository
participant Database

User->>API: GET /places
API->>Facade: get_places(filters)
Facade->>Service: process_filters(filters)
Service->>Repository: fetch_places(filters)
Repository->>Database: SELECT * FROM places
Database-->>Repository: places data
Repository-->>Service: list of places
Service-->>Facade: formatted data
Facade-->>API: response
API-->>User: 200 OK
```

---

### Explanation

All API calls follow a consistent interaction flow:

User → API → Facade → Service → Repository → Database → Response

#### Key Points

- **API Layer** handles incoming requests
- **Facade** simplifies access to business logic
- **Service Layer** processes logic and validation
- **Repository Layer** handles database operations
- **Database** stores persistent data

---

## 5. Conclusion

This document provides a structured overview of the HBnB system architecture and design.

It ensures:
- Clear separation of concerns
- Scalable and maintainable architecture
- Consistent interaction patterns across the system

The diagrams and explanations serve as a reliable reference for development and future enhancements.
