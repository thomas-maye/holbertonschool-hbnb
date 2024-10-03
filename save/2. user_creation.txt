sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Register new account
    API->>BusinessLogic: Validate User data
    BusinessLogic->>Database: Check if user exists already in data
    Database-->>BusinessLogic: User not founded
    BusinessLogic->>Database: Save new user in data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return success of the registration
    API-->>User: Registration success
