# QR Code Attendance System

## Project Overview

The QR Code Attendance System is a modern, efficient solution designed to automate and streamline attendance tracking in educational or corporate environments. By leveraging dynamic QR code generation and seamless integration with Google Sheets, this system eliminates the need for manual record-keeping, reducing administrative overhead and enhancing data accuracy. It provides a robust and user-friendly platform for both instructors (teachers/admins) to manage sessions and for participants (students) to record their attendance effortlessly.

## Key Features & User Experience

*   **Dynamic Session Management:** Instructors can easily initiate new attendance sessions by providing a unique session name. This action dynamically creates a dedicated worksheet within a central Google Sheet, ensuring organized and accessible records.
*   **Intuitive QR Code Generation:** Upon session creation, a unique QR code is instantly generated. The teacher interface features a dynamic layout that transitions smoothly from a single column to a responsive two-column view on larger screens, presenting the QR code with a captivating "screen open" animation.
*   **Effortless Student Attendance:** Students use their personal mobile devices to scan the displayed QR code. This redirects them to a streamlined web form where their session details are pre-filled, allowing for quick and accurate attendance submission.
*   **One-Time Attendance Enforcement:** The system intelligently prevents duplicate attendance entries, ensuring each student can mark their presence only once per session.
*   **Real-time Data Storage:** All attendance records, including student name, roll number, date, and time, are securely stored and instantly updated in the designated Google Sheet worksheets.
*   **Responsive and Animated Interface:** Both teacher and student interfaces are designed with a clean, modern aesthetic, featuring responsive layouts that adapt seamlessly across various devices. Interactive elements, such as animated buttons and visual feedback for attendance submission, enhance the overall user experience.

## Technical Stack

This project is built upon a robust and scalable technical foundation:

**Frontend:**
*   **HTML5, CSS3, JavaScript (ES6+):** For structuring content, styling, and implementing interactive client-side logic.
*   **Material UI (via CDN):** Provides a comprehensive set of pre-designed, responsive, and customizable UI components, ensuring a consistent and aesthetically pleasing user experience.

**Backend:**
*   **Python 3.x:** The core language for server-side logic.
*   **Flask:** A lightweight and flexible micro-web framework for Python, used to build RESTful API endpoints.
*   **`qrcode` and `Pillow`:** Python libraries for efficient generation and image manipulation of QR codes.
*   **`gspread`:** A Python client library for the Google Sheets API, enabling programmatic access and manipulation of spreadsheet data.
*   **`oauth2client`:** Facilitates secure authentication with Google APIs using service account credentials.
*   **`gspread_formatting`:** Extends `gspread` capabilities to allow advanced formatting of Google Sheets cells and worksheets.

## System Architecture

The system employs a clear client-server architecture, facilitating distinct workflows for instructors and students. The core components and their interactions are detailed below, visualized by the accompanying Mermaid diagram:

*   **Teacher Browser (`frontend/teacher.html`):** The primary interface for instructors to initiate attendance sessions. It allows for entering a session name, which triggers the backend to create a new attendance sheet and generate a unique QR code. The interface dynamically adapts, providing a dedicated area for QR code display after generation.
*   **Student Phone's Native QR Scanner:** Students utilize their mobile device's built-in QR scanner to read the QR code displayed by the instructor. This action automatically redirects them to the student attendance submission form.
*   **Student Browser (`frontend/index.html`):** This is the student-facing interface where attendance is recorded. Upon redirection from the QR scan, the session details are pre-populated, and students submit their name and roll number. The interface provides animated feedback for submission status.
*   **Backend (Flask API):** A Python Flask application that serves as the central API server. It handles requests for session creation, QR code generation, and attendance submission. It orchestrates interactions with Google Sheets to manage attendance data.
*   **Google Sheets (Main Spreadsheet):** Serves as the persistent data store for all attendance records. It houses a main spreadsheet, which then contains multiple individual worksheets for each specific session.
*   **Session Specific Worksheet:** Each unique attendance session (e.g., "MATH_CLASS_20250926") is managed within its own worksheet inside the main Google Sheet. These worksheets are dynamically created and structured with essential columns like "Student Name", "Roll No", "Date", and "Time".

```mermaid
flowchart TD
    TeacherBrowser("Teacher Browser (frontend/teacher.html)")
    StudentPhoneScanner("Student Phone's Native QR Scanner")
    StudentBrowser("Student Browser (frontend/index.html)")
    Backend("Backend (Flask API)")
    GoogleSheets("Google Sheets (Main Spreadsheet)")
    SessionWorksheet("Session Specific Worksheet")

    TeacherBrowser --> Backend: (1. Start Session & Create Sheet)
    Backend -- New Sheet URL --> GoogleSheets
    Backend -- QR Image --> TeacherBrowser
    TeacherBrowser -- Displays QR --> StudentPhoneScanner
    StudentPhoneScanner -- Scans QR & Redirects --> StudentBrowser: (with session name in URL)
    StudentBrowser -- Submits Attendance --> Backend
    Backend -- Records Attendance --> SessionWorksheet
    GoogleSheets --> SessionWorksheet
```

## Setup and Local Deployment

To get a local copy of this project up and running, follow these steps. This guide covers setting up Google Sheets API credentials, configuring the backend, and launching the frontend.

### Prerequisites

Ensure you have the following installed on your system:

*   **Python 3.x**
*   **pip** (Python package installer)
*   **Git** (for cloning the repository)
*   A **web browser**
*   A **Google Account** with access to Google Sheets

### 1. Google Sheets API Configuration

This system relies on the Google Sheets API for attendance data storage. You'll need to create a Google Cloud Project, enable the Sheets API, and set up a service account for secure access.

1.  **Google Cloud Console Access:** Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2.  **Project Selection/Creation:**
    *   Select an existing project or create a new one.
    *   Ensure the selected project is active for all subsequent steps.
3.  **Enable Google Sheets API:**
    *   In the search bar, type "Google Sheets API" and select it from the results.
    *   Click the "Enable" button.
4.  **Create Service Account Credentials:**
    *   Go to "APIs & Services" > "Credentials".
    *   Click "+ Create Credentials" and choose "Service Account".
    *   Provide a descriptive "Service account name" (e.g., `qr-attendance-service`).
    *   Grant the service account an appropriate role, such as "Project > Editor" (for development convenience; consider more granular roles like "Sheets Editor" for production environments).
    *   Click "Done" to complete service account creation.
5.  **Generate JSON Key File (`creds.json`):**
    *   From the "Credentials" page, click on the newly created service account.
    *   Go to the "Keys" tab.
    *   Click "Add Key" > "Create new key".
    *   Select "JSON" as the key type and click "Create". This will download a JSON file containing your service account's private key. **Rename this file to `creds.json`**.
6.  **Place `creds.json`:** Move the downloaded `creds.json` file into the `backend/` directory of your project. The application expects this file at `Jagran-Training/backend/creds.json`.
7.  **Share Google Sheet with Service Account:**
    *   Create a new Google Sheet (or use an existing one) that will serve as the main "QR Attendance Records" spreadsheet. This sheet will dynamically host individual session worksheets.
    *   Open this Google Sheet, click the "Share" button.
    *   Locate the **"Client Email"** field within your `creds.json` file (it typically looks like `your-service-account-name@your-project-id.iam.gserviceaccount.com`).
    *   Paste this email address into the "Add people and groups" field in Google Sheets, grant "Editor" permissions, and click "Send". This step is crucial for the backend to access and modify your spreadsheet.

### 2. Backend Setup

1.  **Navigate to Backend Directory:** Open your terminal or command prompt and change your directory to the `backend/` folder:
    ```bash
    cd backend
    ```
2.  **Install Dependencies:** It's highly recommended to use a virtual environment for Python projects. Activate your virtual environment (if using one) and then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Flask Application:** Start the backend server:
    ```bash
    python app.py
    ```
    *   The server will typically run on `http://127.0.0.1:5000/`. Ensure it starts without errors.

### 3. Frontend Access

With the backend running, you can now access the frontend interfaces:

1.  **For Instructors (Teacher Page):** Open `frontend/teacher.html` in your web browser. This page is used to start sessions and generate QR codes.
2.  **For Students (Attendance Form):** Students will access `frontend/index.html` via their mobile phone's QR scanner after scanning a teacher-generated QR code. Alternatively, you can open this file directly in a browser for testing (e.g., `http://localhost:8000/frontend/index.html?qr_data=TEST_SESSION_NAME`, adjusting the hostname/port if needed). Ensure the backend server (`http://127.0.0.1:5000/`) is accessible from where the frontend is being served for API calls to succeed.

## Troubleshooting

*   **`Connection refused` or `Failed to fetch` errors:** Ensure your Flask backend (`app.py`) is running. Check the terminal where you started the backend for any error messages.
*   **Google Sheets API errors (e.g., `Insufficient Permission`, `Worksheet Not Found`):**
    *   Verify that the Google Sheets API is enabled in your Google Cloud Project.
    *   Confirm that the service account email (from `creds.json`) has "Editor" access to your main "QR Attendance Records" Google Sheet.
    *   Double-check that `creds.json` is correctly placed in the `backend/` directory and the file name matches exactly.
    *   Ensure the spreadsheet name in `backend/app.py` and `backend/sheet_manager.py` exactly matches your Google Sheet's name.
*   **`ImportError: attempted relative import with no known parent package`:** This usually means you're running a Python file directly that expects to be part of a package. Ensure your imports are correct (`from sheet_manager import SheetManager` instead of `from .sheet_manager import SheetManager` if `app.py` is run as a script directly).

## Usage

This section outlines the workflow for both instructors and students, detailing how to utilize the QR Code Attendance System for session management and attendance recording.

### For Instructors (Session Management & QR Generation)

1.  **Access the Teacher Interface:** Open `frontend/teacher.html` in your web browser.
2.  **Start a New Session:** Enter a unique **Session Name** (e.g., `MATH_CLASS_20250926`, `CHEMISTRY_LAB_GROUP_A`) into the designated input field.
    *   This action triggers the backend to create a new worksheet with this name within your main "QR Attendance Records" Google Sheet, pre-configured with "Student Name", "Roll No", "Date", and "Time" columns.
3.  **Generate QR Code:** Click the "Start Session & Generate QR Code" button.
    *   A unique QR code will be displayed, dynamically generated to embed the student attendance URL with the session name. This QR code is ready for students to scan.

### For Students (Attendance Submission)

1.  **Scan QR Code:** Using your mobile phone's native QR code scanner, scan the QR code displayed by your instructor.
2.  **Access Attendance Form:** You will be automatically redirected to the `frontend/index.html` page in your phone's browser.
3.  **Submit Attendance:**
    *   The **Session Name** from the scanned QR code will be automatically populated in a hidden field.
    *   Enter your **Name** and **Roll Number** in the respective fields.
    *   Click "Submit Attendance".
4.  **Confirmation:**
    *   Upon successful submission, your attendance record (Name, Roll No, Date, Time) will be saved to the corresponding session's worksheet in Google Sheets.
    *   The system enforces one-time attendance per student per session; if you attempt a duplicate submission, you will be notified accordingly.

## Future Enhancements

Potential future features and improvements for the QR Code Attendance System:

*   **Instructor Dashboard:** Implement a dedicated web interface for instructors to view, manage, and export attendance records directly from the application, eliminating the need to interact directly with Google Sheets for daily operations.
*   **User Authentication & Authorization:** Introduce a robust authentication system for instructors and potentially students, with role-based access control.
*   **Hybrid Authentication:** Explore integrating advanced authentication methods like facial recognition alongside QR code scanning for enhanced security and convenience.
*   **Session Scheduling & Management:** Allow instructors to schedule sessions in advance, set attendance windows, and manage session lifecycles more comprehensively.
*   **Reporting & Analytics:** Develop features for generating attendance reports, statistics, and insights.
*   **Notifications:** Implement email or in-app notification systems for attendance status, session updates, etc.

## Contributing

We welcome contributions to enhance this project! If you'd like to contribute, please follow these guidelines:

1.  **Fork the repository:** Start by forking the project to your GitHub account.
2.  **Create a new branch:** Create a new branch for your feature or bug fix (e.g., `feature/add-dashboard`, `bugfix/fix-attendance-issue`).
3.  **Implement your changes:** Write clear, concise code and ensure it adheres to the project's coding standards.
4.  **Test thoroughly:** Before submitting, ensure your changes are well-tested and do not introduce new issues.
5.  **Commit your changes:** Write clear and descriptive commit messages.
6.  **Open a Pull Request:** Submit a pull request to the `main` branch of this repository, describing your changes in detail.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details. (Note: A `LICENSE.md` file would need to be created if this project were open-sourced.)

