# Theater Project

## Description
This is a theater management project built with Django. It includes background task management, QR code generation, and a production-ready configuration.

## Prerequisites

Before setting up the project, ensure that you have the following installed:

- Python 3.9 or above
- Poetry (for dependency management)
- Redis (if using Huey with Redis)

## Installation and Setup

1. **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd theater
    ```

2. **Set up the virtual environment**:

    ```bash
    poetry install
    ```

3. **Switch to the `dev` branch** (for development):

    ```bash
    git checkout dev
    ```

4. **Apply Migrations**:

    ```bash
    python manage.py makemigrate
    python manage.py migrate
    ```

5. **Run the development server**:

    ```bash
    python manage.py runserver
    ```
