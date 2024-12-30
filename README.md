# University Management System

This is a system designed to manage various aspects of a university, including students, professors, courses, subjects, contracts, grades, and trimester summaries. Below is a description of the models that are used to structure the data.

## Models

### Student Model

Represents student information.

- **first_name**: First name of the student (required).
- **last_name**: Last name of the student (required).
- **full_name**: Computed full name based on first and last name (stored).
- **date_of_birth**: Date of birth (required).
- **age**: Computed age (stored).
- **gender**: Gender selection: Male, Female, Other (required).
- **departments**: Department/faculty to which the student belongs (required).
- **trimester**: Current trimester (required).
- **career**: Career the student is enrolled in (required).
- **active**: Boolean field indicating whether the student is active.
- **email**: Student's email address (required).

### Professor Model

Represents professor information.

- **first_name**: First name of the professor.
- **last_name**: Last name of the professor.
- **full_name**: Computed full name based on first and last name (stored).
- **age**: Age of the professor.
- **time_in_university**: Number of years the professor has been at the university.
- **is_tenured**: Boolean indicating whether the professor is tenured.
- **is_available**: Boolean indicating whether the professor is available.
- **current_courses**: Computed number of courses assigned to the professor.
- **max_courses**: Maximum number of courses a professor can handle.
- **subjects**: Subjects that the professor is teaching.
- **email**: Professor's email address (required).

### Student Contract Model

Represents contracts between students and the university.

- **student_id**: The student associated with the contract (required).
- **subject_ids**: The subjects the student is enrolled in (required).
- **professor_ids**: The professors assigned to the subjects (required).
- **price**: The price of the contract (required).
- **room**: The room where the course will be held (required).
- **payment_status**: The payment status (Pending, Paid, Overdue).
- **creation_date**: The creation date of the contract.
- **professor_hours**: Computed hours the professor will spend per trimester.

### Subject Option Model

Represents subject options available for students.

- **name**: Name of the subject (required).
- **code**: Unique code for the subject (required).
- **career_ids**: Careers that include this subject.

### Subject Model

Represents individual subjects in the university.

- **career_id**: The career the subject is part of (required).
- **trimester**: Trimester in which the subject is offered.
- **name**: Name of the subject (required).
- **code**: Code for the subject.
- **hours_per_week**: Number of hours the subject is taught per week (required).
- **trimester_duration**: Duration of the trimester in weeks.
- **hours_per_trimester**: Computed hours the subject lasts per trimester.
- **professor_ids**: Professors assigned to the subject.

### Career Model

Represents a career in the university.

- **name**: Name of the career (required).
- **department**: Faculty/department associated with the career (required).
- **code**: Unique code for the career (required).
- **duration_years**: Duration of the career in years (required).
- **description**: Brief description of the career.
- **active**: Boolean indicating whether the career is active.
- **subject_ids**: Subjects that are part of this career.
- **total_subjects**: Computed total number of subjects in the career.

### Grade Model

Represents the grades received by students in their subjects.

- **student_id**: The student who received the grade (required).
- **subject_id**: The subject for which the grade was given (required).
- **trimester**: Trimester during which the subject was taken (required).
- **grade**: The grade received by the student (required).
- **professor_feedback**: Feedback from the professor.

### Trimester Summary Model

Represents a summary of the student's performance during a trimester.

- **student_id**: The student associated with the summary (required).
- **trimester**: Trimester for which the summary is generated (required).
- **average_grade**: Computed average grade for the student in that trimester.
- **professor_feedback_average**: Computed average feedback from professors.
- **approved_subjects**: Number of subjects the student has passed.
- **failed_subjects**: Number of subjects the student has failed.
- **grade_ids**: List of grades associated with the student.

### Consolidated Table Model

Represents a consolidated view of contracts, professors, and student-related data.

- **student_id**: The student associated with the table.
- **subject_id**: The subject associated with the table.
- **professor_id**: The professor associated with the subject.
- **contract_id**: The contract associated with the student.
- **price**: The price of the contract.
- **room**: The room where the subject is taught.
- **payment_status**: The payment status (Pending, Paid, Overdue).
- **trimester**: Trimester of the student.
- **gender**: Gender of the student.
- **departments**: Faculty/department of the student.
- **career**: Career of the student.
- **active**: Boolean indicating whether the student is active.
- **total_contracts**: Computed total number of contracts.
- **total_payments**: Computed total payments.
- **active_contracts**: Computed number of active contracts.
- **total_professors**: Computed total number of professors.

## Running the Code

Follow the steps below to set up and run the system:

1. **Create a Python Virtual Environment:**

   To start, create a virtual environment using `venv`:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment:**
   After creating the environment, activate it using the appropriate command for your system:

   - On macOS/Linux:

   ```
   source venv/bin/activate
   ```

   - On Windows:

   ```
   .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   With the virtual environment activated, install the required dependencies from the requirements.txt file:

   ```
   pip install -r requirements.txt
   ```

4. **Run the Code:**
   Finally, run the application with the following command:
   `   python3 odoo/odoo-bin -c conf/odoo.conf`
   This will start the system with the provided configuration file odoo.conf.
