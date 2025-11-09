# Django project follows (DDD) Architecture

This project follows Domain-Driven Design principles with a clean architecture structure.


## Architecture Layers


### 1. Domain Layer (`src/domain/`)
The core business logic layer. Contains:

- **Entities**: Domain objects with identity (e.g., `User`)
- **Value Objects**: Immutable objects defined by their attributes (e.g., `Email`, `Username`)
- **Domain Services**: Business logic that doesn't naturally fit in entities
- **Repository Interfaces**: Contracts for data access (ports)
- **Domain Events**: Events that represent something that happened in the domain



### 2. Application Layer (`src/application/`)
Orchestrates domain objects to perform application tasks. Contains:

- **Use Cases**: Application services that coordinate domain objects
- **DTOs**: Data Transfer Objects for communication between layers



### 3. Infrastructure Layer (`src/infrastructure/`)
Implements technical concerns. Contains:

- **Repository Implementations**: Concrete implementations of domain repositories (adapters)
- **Event Publishers**: Implementation of domain event publishing
- **Dependency Injection**: Service container for managing dependencies


### 4. Presentation Layer (`src/authentication/views.py`, `src/api/`)
Handles HTTP requests and responses. Contains:

- **API Views**: REST API endpoints
- **Serializers**: Request/response validation and transformation



## Scale

## Tips

1. **Start with Domain**: Always design domain layer first (business logic)
2. **Keep Domain Pure**: No Django imports in domain layer
3. **Use Value Objects**: For validation and type safety
4. **Repository Pattern**: Always use interfaces in domain
5. **Use Cases**: One use case = one operation
6. **DTOs**: Use DTOs for layer communication
7. **Events**: Use for decoupled communication


For **EVERY** new bounded context, follow these steps:

1. **Domain Layer** (`src/domain/{context}/`)
   - `entities.py` - Domain entities (aggregate roots)
   - `value_objects.py` - Value objects
   - `repositories.py` - Repository interfaces
   - `services.py` - Domain services
   - `events.py` - Domain events

2. **Application Layer** (`src/application/{context}/`)
   - `use_cases.py` - Application use cases
   - Add DTOs to `shared/dtos.py`

3. **Infrastructure Layer** (`src/infrastructure/persistence/`)
   - `{context}_repository.py` - Repository implementation
   - Update `dependency_injection/container.py`

4. **Presentation Layer** (`src/{context}/`)
   - `models.py` - Django ORM models (if needed)
   - `views.py` - API views
   - `urls.py` - URL routing
   - Register in `src/api/urls.py` and `config/django/base.py`
