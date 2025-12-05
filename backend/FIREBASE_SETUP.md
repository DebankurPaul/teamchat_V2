# How to Get Your Firebase Service Account Key

The `serviceAccountKey.json` file is a credential that allows your backend server to authenticate with Firebase securely.

## Step 1: Create a Firebase Project
1.  Go to the [Firebase Console](https://console.firebase.google.com/).
2.  Click **"Create a project"** (or select an existing one).
3.  Follow the setup steps (you can disable Google Analytics for now).

## Step 2: Create a Firestore Database
1.  In your project dashboard, go to **"Build"** > **"Firestore Database"** in the left menu.
2.  Click **"Create database"**.
3.  Choose a location (e.g., `nam5 (us-central)`).
4.  **Important**: Start in **Test mode** (allows read/write access for development).
5.  Click **Create**.

## Step 3: Generate the Key
1.  Click the **Gear icon** (Settings) next to "Project Overview" in the top left.
2.  Select **"Project settings"**.
3.  Go to the **"Service accounts"** tab.
4.  Under "Firebase Admin SDK", click **"Generate new private key"**.
5.  Click **"Generate key"** to download the JSON file.

## Step 4: Add to Project
1.  Rename the downloaded file to `serviceAccountKey.json`.
2.  Move this file into the `backend/` folder of your project:
    `c:\Users\Lenovo\Desktop\new_agent\backend\serviceAccountKey.json`

> [!WARNING]
> Keep this file secret! Do not share it or commit it to public repositories.
