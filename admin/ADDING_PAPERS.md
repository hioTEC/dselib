# How to Add New Papers to DSE Lib Mirror

This system is designed to be **static** and **zero-maintenance**. You do not need to run a database or write SQL.

## 1. Prepare Your Files
Rename your files to follow a recognizable convention. The system automatically detects the year and exam type.

**Naming Convention:**
- **Year**: Must contain 4 digits (e.g., `2024`, `1998`).
- **File Type**: 
    - `p1`, `paper1` -> Paper 1
    - `ans`, `marking` -> Marking Scheme
    - `per`, `report` -> Exam Report

## 2. Drop Files into `downloads/`
Navigate to the `downloads` folder in the project root.

1.  Find the subject folder (e.g., `downloads/Physics`).
2.  Find or create the Exam Type folder (`DSE`, `CE`, `AL`).
3.  Find or create the Language folder (`ENG`, `CHI`).
4.  Find or create the **Year** folder (e.g., `2024`).
5.  **Paste your file there.**

**Example Path:**
`d:\CODING\dselib\downloads\Physics\DSE\ENG\2024\2024_Physics_Paper1.pdf`

## 3. Update the Website
After adding files, you must update the `data.json` index so the website knows about them.

1.  Open a terminal in the project root `d:\CODING\dselib`.
2.  Run the indexer script:
    ```bash
    python indexer.py
    ```
3.  Wait for it to finish. It will say `索引生成完成!`.

## 4. Done!
Refresh your `index.html` in the browser. The new papers will appear immediately.
