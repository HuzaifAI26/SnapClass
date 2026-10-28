# SNAPCLASS — AI-Powered Smart Attendance System

An AI-powered attendance management application that combines **facial recognition and voice-based speaker identification** to help teachers generate attendance records. Built with Python and Streamlit, with Supabase for database management.

<!-- Add a project screenshot here -->
<!-- ![SNAPCLASS Dashboard](docs/images/dashboard.png) -->

## Overview

Traditional classroom attendance can be time-consuming and may require teachers to mark students manually. SNAPCLASS aims to simplify this process by using AI-based biometric identification to generate attendance predictions from classroom photos or audio recordings.

The application provides teacher and student workflows, subject enrollment, AI-assisted attendance processing, attendance review, and database-backed attendance records.

**Important:** AI-generated attendance is a prediction and should be reviewed before it is saved.

## Key Features

- **Teacher authentication:** Teacher registration and login with bcrypt-based password hashing and verification.
- **Student management:** Store student profiles and associated biometric embeddings.
- **Subject management:** Create subjects and manage student enrollment using subject codes.
- **Face-based attendance:** Detect faces in classroom images, extract face embeddings, and classify student identities.
- **Voice-based attendance:** Generate speaker embeddings from audio and compare them with enrolled voice profiles.
- **Attendance review:** Review generated attendance results before confirming or discarding them.
- **Database integration:** Store student information, subject enrollment, biometric profiles, and attendance records using Supabase.
- **Attendance reports:** View attendance records associated with a teacher's subjects.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| Face detection | dlib |
| Face feature extraction | Pretrained dlib face-recognition model |
| Face classification | scikit-learn SVM |
| Voice feature extraction | Resemblyzer |
| Audio processing | librosa |
| Numerical processing | NumPy |
| Data presentation | Pandas |
| Database | Supabase / PostgreSQL |
| Password security | bcrypt |

## AI/ML Methodology

### 1. Facial Recognition Pipeline

SNAPCLASS uses face embeddings to represent detected faces numerically and a Support Vector Machine (SVM) to classify student identities.

**Workflow:**

1. Input a classroom image.
2. Detect faces using dlib's frontal face detector.
3. Estimate facial landmarks using a shape predictor.
4. Generate a 128-dimensional face descriptor using the pretrained dlib face-recognition model.
5. Use a linear SVM trained on stored student embeddings to predict an identity.
6. Compare the predicted student's stored embedding with the detected face using Euclidean distance.
7. Accept the match when the distance satisfies the configured threshold of `0.6`.

**Why use embeddings?**

Face embeddings represent facial features as numerical vectors. This allows the system to compare faces and use a conventional ML classifier rather than training a deep-learning model from scratch.

**Current implementation notes:**
- The SVM is trained from the student embeddings retrieved from the database.
- The implementation uses a distance threshold to help reject uncertain identity matches.
- The current distance check compares against the first stored embedding for the predicted student; comparing against all available samples would be a useful improvement.
- The threshold should be validated using representative images before real-world deployment.

### 2. Voice-Based Speaker Identification

SNAPCLASS uses Resemblyzer to generate speaker embeddings and compares an audio sample with stored student voice profiles.

**Workflow:**

1. Capture or upload an audio recording.
2. Load and resample the audio to 16 kHz using librosa.
3. Detect non-silent audio segments.
4. Ignore segments shorter than 0.5 seconds in the bulk-processing workflow.
5. Generate speaker embeddings using Resemblyzer.
6. Compare each embedding with enrolled voice embeddings using a dot-product similarity score.
7. Accept a speaker match when the best score meets the configured threshold of `0.65`.

**Important distinction:** This pipeline identifies a speaker from voice characteristics. It does not transcribe speech or verify that the person explicitly said a particular attendance phrase.

The similarity threshold must be evaluated with real recordings to understand false matches and missed matches.

### 3. Attendance Generation and Confirmation

After biometric identification, the application generates attendance results for the selected subject.

- Identified students are marked as present in the generated results.
- The current workflow marks other enrolled students as absent.
- The teacher reviews the results.
- Selecting **Confirm & Save** inserts the attendance records into Supabase.
- Selecting **Discard** clears the pending results without saving them.

The application uses teacher review as a safeguard before committing generated attendance records. However, the current absent-by-default behavior can produce incorrect absences when a student is not detected.

## System Architecture

```text
                Teacher / Student
                       |
                       v
                Streamlit UI
                       |
          +------------+------------+
          |                         |
          v                         v
   Face Attendance            Voice Attendance
          |                         |
          v                         v
    dlib Detection            librosa Processing
          |                         |
          v                         v
   Face Embeddings          Resemblyzer Embeddings
          |                         |
          v                         v
      Linear SVM              Similarity Matching
          |                         |
          +------------+------------+
                       |
                       v
              Attendance Results
                       |
                       v
              Teacher Confirmation
                       |
                       v
                Supabase Database
```

## Project Structure

The following is an illustrative structure based on the modules reviewed so far. Update it to match the actual files in your GitHub repository.

```text
SNAPCLASS/
├── .devcontainer/
├── assets/
├── src/
│   ├── components/
│   │   ├── __pycache__/
│   │   ├── dialog_add_photo.py
│   │   ├── dialog_attendance_results.py
│   │   ├── dialog_auto_enroll.py
│   │   ├── dialog_create_subject.py
│   │   ├── dialog_enroll.py
│   │   ├── dialog_share_subject.py
│   │   ├── dialog_voice_attendance.py
│   │   ├── footer.py
│   │   ├── header.py
│   │   └── subject_card.py
│   ├── database/
│   │   ├── __pycache__/
│   │   ├── config.py
│   │   └── db.py
│   ├── pipelines/
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   ├── screens/
│   │   ├── __pycache__/
│   │   ├── home_screen.py
│   │   ├── student_screen.py
│   │   └── teacher_screen.py
│   └── ui/
├── .gitignore
├── app.py
└── requirements.txt
```

Add any other directories and files that exist in your repository, including the actual location of your face and voice processing modules.

## Database Overview

SNAPCLASS uses Supabase, backed by PostgreSQL, for persistent application data.

The reviewed code interacts with these data entities:

- **Students:** Student profiles and stored face or voice embeddings.
- **Teachers:** Teacher account information and password hashes.
- **Subjects:** Subject details, teacher association, and subject codes.
- **Subject enrollment:** Relationships between students and subjects.
- **Attendance logs:** Attendance status, subject, student, and timestamp.

The exact schema and constraints should be documented from the database configuration used by the project.

## Installation and Setup

### Prerequisites

- Python installed in a version supported by the project's dependencies.
- Git.
- A Supabase project with the required database tables and permissions.
- Compatible versions of dlib, scikit-learn, Resemblyzer, librosa, and Streamlit.

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

If your repository contains a complete and tested `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If the file is missing, create it from the project's actual dependencies and test the installation before publishing setup instructions. Packages such as dlib can require additional build tools depending on the operating system and Python version.

### 4. Configure Supabase credentials

Create the following file:

```text
.streamlit/secrets.toml
```

Add your own credentials:

```toml
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
```

The application reads these values through `st.secrets`.

**Security:** Never commit real credentials, service-role keys, or other secrets to GitHub. Use an appropriate restricted key and configure Supabase Row Level Security (RLS) and authorization policies for your application's access patterns.

### 5. Run the application

Use the Streamlit entry-point file that is actually configured in your repository. For example, if `teacher_screen.py` is the main entry point:

```bash
streamlit run app.py
```

If your project uses another main application file, replace the command accordingly.

## How to Use SNAPCLASS

The intended workflow is:

1. Register or log in as a teacher.
2. Create a subject and share its subject code with students.
3. Enroll students in the relevant subject.
4. Ensure each student's required biometric profile is available.
5. Select a subject and process classroom photos or audio.
6. Review the generated attendance results.
7. Confirm and save the results, or discard them.
8. Open the attendance records section to review saved records.

Some enrollment and photo-upload paths still need end-to-end verification. Confirm that the files in the published repository support every step before describing this workflow as fully operational.

## Limitations and Considerations

- **Recognition accuracy:** Face and voice thresholds require testing on representative data.
- **False attendance results:** Lighting, face angle, background noise, overlapping speakers, and short recordings can affect identification.
- **Unknown identities:** A classifier can predict a known student even when the input belongs to someone unknown; threshold-based rejection is not a guarantee.
- **Absence handling:** Failure to identify a student does not necessarily mean that the student is absent.
- **Voice identification:** Speaker similarity does not prove what words were spoken or that the audio is a live, genuine recording.
- **Data privacy:** Face images, voice recordings, and biometric embeddings require appropriate consent, access control, retention policies, and secure storage.
- **Database security:** Authentication in the application should be supported by appropriate database authorization and RLS policies.
- **Duplicate records:** Attendance sessions should have suitable duplicate-prevention and consistency checks.

## Future Improvements

- Evaluate face and voice identification using representative test datasets.
- Measure false acceptance and false rejection rates.
- Compare each detected face with all available samples for the predicted student.
- Improve handling of unknown identities and uncertain attendance results.
- Add an explicit review state for students whose attendance could not be verified.
- Improve voice processing for overlapping speech and noisy classroom recordings.
- Add attendance-session identifiers and duplicate-record protection.
- Add automated tests, logging, and error handling.
- Strengthen database authorization and biometric data protection.
- Verify the full enrollment and photo-upload workflows.

## Privacy and Responsible Use

SNAPCLASS processes biometric information, which can be sensitive personal data. Use it only with appropriate consent and authorization. Protect credentials and biometric profiles, restrict database access, and establish clear data retention and deletion procedures.

AI-generated results should be reviewed by an authorized teacher before attendance is finalized.

## Author

**Your Name**

- GitHub: [Huzaifa Ansari](https://github.com/HuzaifAI26)
- LinkedIn: [Huzaifa Ansari](www.linkedin.com/in/huzaifaansari-ai)


