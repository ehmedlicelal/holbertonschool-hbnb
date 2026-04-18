# Sequence Diagrams for API Calls

## 1. User Registration

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant Service
participant Repository
participant Database

User->>API: POST /users (register)
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

## 2. Place Creation

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

## 3. Review Submission

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

## 4. Fetch List of Places

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
API-->>User: 200 OK (places list)
```

---

## Summary

All API calls follow this architecture:

User → API → Facade → Service → Repository → Database → Response

- **Presentation Layer:** API  
- **Business Logic Layer:** Facade + Service  
- **Persistence Layer:** Repository + Database  

The **Facade pattern** ensures a clean and simple interface between layers.
