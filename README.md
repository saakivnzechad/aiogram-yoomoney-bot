![Project Status](https://img.shields.io/badge/Status-Completed-green.svg)
![Technologies](https://img.shields.io/badge/Tech-Python%2C%20Aiogram%2C%20SQLite%2C%20YooMoney-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

# Telegram Bot for Automated Digital Content Sales (Commercial Project)

A Multifunctional Telegram Bot with Payment System Integration

---

## Project Overview

This repository contains the code for a Telegram bot developed to automate the sales and delivery processes of digital content. The project demonstrates my skills in Python bot development using the Aiogram framework, as well as integration with external APIs like the YooMoney payment system.

The bot provides users with a convenient interface to access various types of content:
* **Free Content**: Available for download or online viewing directly from the bot.
* **Paid Digital Product**: Purchase is made via integration with the YooMoney API, with automatic payment status verification and subsequent content delivery.

Special attention has been paid to **payment security and reliability**: a unique identifier (token) is generated for each transaction and linked to the user's Telegram ID in the SQLite database. The system automatically verifies the payment success using this token and manages access to paid content, taking into account previously completed payments. User session and dialogue management are implemented using Finite State Machines (FSM).

**Important Note:** This project was developed for a real commercial client. To maintain client confidentiality and intellectual property, **all sensitive data (API tokens, specific content links, and contact information) have been anonymized and replaced with placeholders**. The provided code demonstrates the bot's full functionality and architecture without revealing private details.

---

## Features

This Telegram bot includes the following key functionalities:

* **Welcome Messages**: Sending interactive welcome messages with images and inline buttons to initiate interaction.
* **Flexible Content Access**:
    * **Free Material**: Users can download or view free documents (e.g., guides, manuals) online.
    * **Paid Product**: A system for selling digital content through secure integration with a payment gateway.
* **YooMoney API Integration**:
    * Generation of unique payment URLs linked to the user's ID.
    * Automatic verification of payment status via the YooMoney API.
    * Payment confirmation and automatic delivery of paid content after a successful transaction.
* **User State Management (FSM)**: Utilization of Aiogram's Finite State Machines for robust control over user dialogue, especially during the payment process.
* **User Database Management (SQLite)**: Storing user information, their payment IDs, and payment statuses to prevent duplicate purchases.
* **Logging**: Detailed logging of all key operations and errors to facilitate debugging and monitoring of the bot's performance.

---

## Technologies Used

The project is built upon the following technology stack:

* **Python**: The primary development language.
* **Aiogram**: An asynchronous framework for Telegram bot development.
* **SQLite**: A lightweight database for storing user data.
* **`yoomoney-api`**: A library for interacting with the YooMoney payment system.
* **`python-dotenv`**: For secure management of environment variables.

---

## Project Structure and Key Files

The main files demonstrating the bot's architecture and logic:

* `bot.py`: The main application file containing the bot's core logic, command and callback handlers, and Finite State Machine (FSM) implementation.
* `config.py`: A module for loading environment variables from the `.env` file, containing all necessary API tokens, links, and payment parameters.
* `.env`: A file for storing confidential environment variables (the repository contains an anonymized version with placeholders).
* `requirements.txt`: A list of all Python dependencies required to run the project.

---

## Setup and Running

To set up and run the bot locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/saakivnzechad/aiogram-yoomoney-bot
    cd aiogram-yoomoney-bot
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # For Windows:
    .\venv\Scripts\activate
    # For macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create the `.env` file:**
    Create a `.env` file in the project's root directory and fill it with the necessary data, using the following structure (placeholders):
    ```env
    API_TOKEN=YOUR_TELEGRAM_BOT_API_TOKEN
    TELEGRAM_CHANNEL_LINK=YOUR_TELEGRAM_CHANNEL_LINK
    FREE_GUIDE_LINK=YOUR_FREE_CONTENT_ONLINE_LINK
    CONTACT_LINK=YOUR_CONTACT_LINK_FOR_CONSULTATION
    PAYMENT_TOKEN=YOUR_YOOMONEY_API_TOKEN
    PAYMENT_SUM=YOUR_PRODUCT_PRICE_IN_RUBLES
    PAYMENT_RECEIVER=YOUR_YOOMONEY_ACCOUNT_NUMBER
    PAYMENT_TARGETS=YOUR_PAYMENT_DESCRIPTION_FOR_YOOMONEY
    ```
    (Note: To run the bot, you will need to obtain real tokens and links from Telegram and YooMoney.)
5.  **Run the bot:**
    ```bash
    python bot.py
    ```
    The bot will start its operation, and you will be able to interact with it on Telegram.

---

## Project Status

This project is considered **completed** and is maintained for portfolio demonstration purposes. It reflects a specific set of skills and architectural decisions applied at the time of its creation. Active development of new features is not planned, however, the repository remains a valuable resource for understanding the implementation of automated bots with payment integration.

---

## Author

**Danil Klimov**
* GitHub: [@saakivnzechad](https://github.com/saakivnzechad)
* Telegram: [@sarthriles](https://t.me/sarthriles)

---

## License

This project is licensed under the **MIT License**. A copy of the license is available in the `LICENSE` file within this repository.