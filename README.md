# Library Management System

This project is a **Library Management System** with two independent API services:

1. **Frontend API** - Used by library users to browse, filter, and borrow books.
2. **Admin API** - Used by admins to manage books and users.

The services communicate using **RabbitMQ** and run in **Docker containers**.

---

## Features

### 🚀 **Frontend API (User Service)**

- Enroll users into the library (email, firstname, lastname)
- List all available books
- Get details of a book by ID
- Filter books by publisher/category
- Borrow books (specify duration in days)

### 🔧 **Admin API**

- Add new books to the catalogue
- Remove books from the catalogue
- List all users in the library
- View users and the books they have borrowed
- List unavailable books (with return date)

### 🔗 **General Requirements Implemented**

- Books borrowed are removed from the available list
- Independent data stores for each API
- **RabbitMQ** for API communication
- **Dockerized deployment**
- Unit & integration tests included

---

## 🛠️ Installation & Setup

### Prerequisites

Make sure you have the following installed:

- **Docker & Docker Compose**
- **Python 3.9+**

### Steps to Run the Project

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Cashie11/Library-Management-System.git
   cd library-management
   ```

2. **Start the Services with Docker:**

   ```bash
   docker-compose up --build
   ```

3. **API Endpoints:**

   - **Frontend API:** [http://localhost:8000](http://localhost:8000)
   - **Admin API:** [http://localhost:8001](http://localhost:8001)

4. **Testing the API:**
   Use **Postman** or **cURL** to test the endpoints.

---

## 📌 API Endpoints

### **Frontend API** (User Service) – `http://localhost:8000`

| Method | Endpoint                                   | Description          |
| ------ | ------------------------------------------ | -------------------- |
| POST   | `/users/`                                  | Enroll a new user    |
| GET    | `/books/`                                  | List available books |
| GET    | `/books/{id}/`                             | Get book details     |
| GET    | `/books/filter?publisher=xyz&category=abc` | Filter books         |
| POST   | `/borrow/{book_id}/`                       | Borrow a book        |

### **Admin API** (Admin Service) – `http://localhost:8001`

| Method | Endpoint              | Description                 |
| ------ | --------------------- | --------------------------- |
| POST   | `/books/`             | Add a new book              |
| DELETE | `/books/{id}/`        | Remove a book               |
| GET    | `/users/`             | List enrolled users         |
| GET    | `/borrowings/`        | List borrowed books         |
| GET    | `/unavailable-books/` | List books with return date |

---

## 🐳 Docker Setup

This project runs in Docker containers using **Docker Compose**.

### Start the Containers

```bash
docker-compose up --build
```

### Stop the Containers

```bash
docker-compose down
```

### View Running Containers

```bash
docker ps
```

---

## ✅ Testing

Run unit tests with:

```bash
docker exec -it library-management-frontend_api-1 pytest
```

Run integration tests with:

```bash
docker exec -it library-management-admin_api-1 pytest
```

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Contributors

- **Ezekude Francis** - [GitHub](https://github.com/Cashie11)

---

## 📩 Contact

For issues or contributions, open a PR or contact me on GitHub.

---

Enjoy coding! 🚀

