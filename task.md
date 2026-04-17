flowchart TB

%% =====================
%% Presentation Layer
%% =====================
subgraph Presentation_Layer["Presentation Layer"]
    UI["User Interface"]
    API["API Controllers"]
end

%% =====================
%% Business Logic Layer
%% =====================
subgraph Business_Logic_Layer["Business Logic Layer"]

    Facade["Facade"]
    Services["Services"]

    subgraph Domain_Models["Domain Models"]
        User["User"]
        Place["Place"]
        Amenity["Amenity"]
        Review["Review"]
    end

end

%% =====================
%% Persistence Layer
%% =====================
subgraph Persistence_Layer["Persistence Layer"]

    Repositories["Repositories"]
    Database["Database"]

end

%% =====================
%% Relationships
%% =====================

UI --> Facade
API --> Facade

Facade --> Services

Services --> User
Services --> Place
Services --> Amenity
Services --> Review

Services --> Repositories

Repositories --> Database
