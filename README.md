# ☕ Smart Cafe & QR Order Management System

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
</div>

---

### 🌟 Project Overview
**Smart Cafe** is a full-stack digital ecosystem designed to modernize restaurant operations. It bridges the gap between traditional service and digital efficiency by offering a seamless QR-based ordering experience for customers and a robust management cockpit for staff.

> **"Built with precision, designed for scale."** This project demonstrates high-level Django architecture, including custom management commands, complex data modeling, and real-time state management.

---

### 🚀 Core Features

#### 📱 Customer Experience (Mobile-First)
*   **QR-Powered Menu**: Scan and browse instantly—no app installation required.
*   **Dynamic Cart System**: Intelligent cart management stored in session state.
*   **Smart Pricing**: Automatic calculation based on servings, weight, and quantities.
*   **Real-time Order Tracking**: Live status updates from 'Pending' to 'Delivered'.
*   **Instant Waiter Call**: Digital signal system with simulated SMS notifications.
*   **Feedback Loop**: Integrated rating system to capture customer satisfaction.

#### 👨‍💼 Management Cockpit (Staff Panel)
*   **High-Level Dashboard**: Real-time business intelligence (Daily revenue, customer flow, active orders).
*   **Table Lifecycle Management**: Visual control over table states (Free 🟢, Occupied 🔴, Cleaning 🟡).
*   **Menu Engineering**: Dynamic management of categories, items, and advertisements.
*   **Order Workflow**: Granular status control for kitchen and service staff.
*   **Staff Roles**: Dedicated roles for Waiters, Chefs, and Administrators.

---

### 🛠 Technical Excellence

| Feature | Implementation Detail |
| :--- | :--- |
| **Backend** | Django 5.0 with robust ORM optimization and prefetching. |
| **Data Integrity** | Complex relationships with `OneToOne`, `ForeignKey`, and `JSONField`. |
| **Automation** | Custom `seed_data` scripts for rapid environment setup. |
| **QR Integration** | Dynamic generation of table-specific access points. |
| **Security** | Role-based access control and secure session management. |
| **Localization** | Fully localized in Uzbek with professional terminology. |

---

### 🏗 Architecture & Design Patterns
*   **Modular App Structure**: Decoupled apps for `core`, `orders`, and `feedback`.
*   **Surgical ORM Queries**: Using `select_related` and `prefetch_related` to minimize DB hits.
*   **Template Composition**: Reusable components via Django template tags and inheritance.
*   **Clean Code**: Adherence to PEP 8 standards and professional naming conventions.

---

### 📦 Quick Start
1.  **Clone & Setup**: 
    ```bash
    git clone https://github.com/SizningUsername/cafe_project.git
    python -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Initialize DB**:
    ```bash
    python manage.py migrate
    python seed_data.py
    python seed_staff.py
    ```
3.  **Run**:
    ```bash
    python manage.py runserver
    ```
    *Access the Admin at `/admin` (admin/admin123) and Staff Panel at `/staff/`.*

---

### 📖 Documentation
Detailed guides for contributors and developers:
*   [**Installation Guide**](./INSTALL.md) - Full step-by-step setup.
*   [**Deployment Guide (Render)**](./DEPLOY.md) - How to go live.
*   [**API & Models**](./DOCS_MODELS.md) - Deep dive into the data structure.

---

### 🤝 Contact & Support
Developed with ❤️ by **[Your Name]**.  
Feel free to reach out for collaboration or inquiries:
- **Telegram**: [@YourUsername]
- **LinkedIn**: [Your Profile]
- **Email**: [your.email@example.com]

---
<div align="center">
  <sub>© 2024 Smart Cafe Project. Released under the MIT License.</sub>
</div>
