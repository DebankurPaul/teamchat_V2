# TeamChat - Real-time Collaboration Platform 🚀

A modern, feature-rich chat application built with React and FastAPI, featuring real-time messaging, file sharing, video calls, and AI-powered content analysis.

## Features ✨

*   **Real-time Messaging**: Instant messaging with WebSocket support (polling fallback).
*   **File Sharing**: Share images, documents, and more with preview support.
*   **AI Analysis**: Analyze shared files and messages for insights and "ideas" using AI.
*   **Video/Voice Calls**: Integrated video and voice calling functionality.
*   **Group Chats**: Create and manage group chats with multiple participants.
*   **Idea Hub**: A dedicated space to track and manage ideas generated from chats.
*   **Calendar View**: Visualize deadlines and events extracted from conversations.
*   **Secure**: Firebase-backed data storage and authentication.

## Tech Stack 🛠️

*   **Frontend**: React, Vite, Tailwind CSS, Lucide React
*   **Backend**: FastAPI, Python, Firebase Admin SDK
*   **Database**: Google Cloud Firestore
*   **AI**: Custom AI service for text and file analysis

## Setup Instructions 📝

### Prerequisites

*   Node.js (v16+)
*   Python (v3.8+)
*   Firebase Project & Service Account Key

### 1. Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Firebase Setup**:
    *   Place your `serviceAccountKey.json` file in the `backend` directory.
    *   Create a `.env` file in the `backend` directory:
        ```env
        FIREBASE_CREDENTIALS=serviceAccountKey.json
        ```
5.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
    The backend will start at `http://localhost:8000`.

### 2. Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
    The frontend will start at `http://localhost:5173`.

## Usage 📱

1.  Open the frontend URL in your browser.
2.  Register or Login (User creation is handled automatically on first login).
3.  Start chatting, creating groups, or sharing files!

## License 📄

This project is licensed under the MIT License.
