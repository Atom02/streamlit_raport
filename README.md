# Student Report Card Generator

A Streamlit application to generate private report cards from CSV/Excel data.

## Features

- **Secure Links**: Generate unique, private links for each student.
- **Easy Updates**: Upload new CSV or Excel files to update scores.
- **Data Privacy**: Option to clear old score data while keeping student links valid.
- **Admin Dashboard**: Manage data and links from a password-protected interface.

## Prerequisites

- Python 3.8+
- pip

## Quick Start

1.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the App**:

    ```bash
    streamlit run app.py
    ```

3.  **Access the Admin Dashboard**:
    - Open the URL shown in the terminal (usually `http://localhost:8501`).
    - Use the default password: `admin123`.

## Usage

1.  **Upload Data**: Upload your exam results (CSV or Excel).
2.  **Generate Links**: The app will generate a list of students with unique links.
3.  **Share**: Copy the link and send it to the respective parent.
4.  **Update**: If scores change, just upload the new file and click "Save to Database (Update)".
5.  **Reset**: Use "Clear All Scores" if you want to start fresh but keep the same student links (useful for new terms).

## File Format

The app expects a specific multi-level header format:

- **Row 1**: Attributes like `Nama Siswa`, `MATEMATIKA`, `IPAS`...
- **Row 2**: Sub-attributes like `TO 1`, `TO 2`...
