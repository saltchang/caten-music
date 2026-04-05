# Clean Architecture

The main idea of Clean Architecture by Robert C. Martin (Uncle Bob) is to separate the concerns of the application into different layers, so that the application is more maintainable and scalable. Here are the main principles of clean architecture from the [original article](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html):

- Independent of Frameworks. The architecture does not depend on the existence of some library of feature laden software. This allows you to use such frameworks as tools, rather than having to cram your system into their limited constraints.
- Testable. The business rules can be tested without the UI, Database, Web Server, or any other external element.
- Independent of UI. The UI can change easily, without changing the rest of the system. A Web UI could be replaced with a console UI, for example, without changing the business rules.
- Independent of Database. You can swap out Oracle or SQL Server, for Mongo, BigTable, CouchDB, or something else. Your business rules are not bound to the database.
- Independent of any external agency. In fact your business rules simply don’t know anything at all about the outside world.

Based on the concept of clean architecture, this project contains the following layers:

Core layer (`/core`): The entities layer, which contains the core business rules and logic
Service layer (`/service`): The use cases layer, which contains the application of business rules and logic
Repository layer (`/repository`): The infrastructure layer, which contains the data access logic
API layer (`/api`): The presentation layer, which contains the HTTP API endpoints
