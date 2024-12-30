import json
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import logging
_logger = logging.getLogger(__name__)


from odoo import api, models, fields, api
from datetime import date
from odoo.tools import float_round
from odoo.exceptions import ValidationError

CAREER_SUBJECTS = {
    'law': {
        1: ['Introduction to Law', 'Legal Writing', 'History of Law'],
        2: ['Civil Law I', 'Criminal Law I', 'Constitutional Law'],
        3: ['Civil Law II', 'Criminal Law II', 'Administrative Law'],
        # Agrega más trimestres según sea necesario
    },
    'medicine': {
        1: ['Anatomy I', 'Physiology I', 'Introduction to Medicine'],
        2: ['Biochemistry', 'Histology', 'Physiology II'],
        3: ['Pathology I', 'Pharmacology I', 'Microbiology'],
        # Agrega más trimestres
    },
    'engineering': {
        1: ['Calculus I', 'Physics I', 'Introduction to Engineering'],
        2: ['Calculus II', 'Physics II', 'Materials Science'],
        3: ['Thermodynamics', 'Strength of Materials', 'Electronics'],
        # Agrega más trimestres
    },
    'arts': {
        1: ['Introduction to Arts', 'History of Arts', 'Drawing I'],
        2: ['Painting I', 'Sculpture I', 'Art Theory'],
        3: ['Drawing II', 'Painting II', 'Contemporary Arts'],
        # Agrega más trimestres
    },
    'science': {
        1: ['General Chemistry', 'Biology I', 'Calculus I'],
        2: ['Organic Chemistry', 'Physics I', 'Calculus II'],
        3: ['Biology II', 'Physics II', 'Statistics'],
        # Agrega más trimestres
    },
    # Agrega más carreras
}

CAREER_OPTIONS = {
            'law': [
                ('law', 'Law'),
                ('international_law', 'International Law')
            ],
            'medicine': [
                ('medicine', 'Medicine'),
                ('nursing', 'Nursing'),
                ('pharmacy', 'Pharmacy')
            ],
            'engineering': [
                ('civil_engineering', 'Civil Engineering'),
                ('mechanical_engineering', 'Mechanical Engineering'),
                ('computer_science', 'Computer Science')
            ],
            'arts': [
                ('fine_arts', 'Fine Arts'),
                ('graphic_design', 'Graphic Design'),
                ('music', 'Music')
            ],
            'science': [
                ('mathematics', 'Mathematics'),
                ('physics', 'Physics'),
                ('chemistry', 'Chemistry')
            ],
            'economics': [
                ('economics', 'Economics'),
                ('business_administration', 'Business Administration'),
                ('accounting', 'Accounting')
            ],
            'education': [
                ('primary_education', 'Primary Education'),
                ('secondary_education', 'Secondary Education'),
                ('pedagogy', 'Pedagogy')
            ],
            'social_sciences': [
                ('sociology', 'Sociology'),
                ('anthropology', 'Anthropology'),
                ('political_science', 'Political Science')
            ],
            'humanities': [
                ('philosophy', 'Philosophy'),
                ('history', 'History'),
                ('literature', 'Literature')
            ],
            'agriculture': [
                ('agronomy', 'Agronomy'),
                ('forestry', 'Forestry'),
                ('veterinary', 'Veterinary Science')
            ]
        }

list_career = [
        ('law', 'Law'),
        ('international_law', 'International Law'),
        ('medicine', 'Medicine'),
        ('nursing', 'Nursing'),
        ('pharmacy', 'Pharmacy'),
        ('civil_engineering', 'Civil Engineering'),
        ('mechanical_engineering', 'Mechanical Engineering'),
        ('computer_science', 'Computer Science'),
        ('fine_arts', 'Fine Arts'),
        ('graphic_design', 'Graphic Design'),
        ('music', 'Music'),
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('economics', 'Economics'),
        ('business_administration', 'Business Administration'),
        ('accounting', 'Accounting'),
        ('primary_education', 'Primary Education'),
        ('secondary_education', 'Secondary Education'),
        ('pedagogy', 'Pedagogy'),
        ('sociology', 'Sociology'),
        ('anthropology', 'Anthropology'),
        ('political_science', 'Political Science'),
        ('philosophy', 'Philosophy'),
        ('history', 'History'),
        ('literature', 'Literature'),
        ('agronomy', 'Agronomy'),
        ('forestry', 'Forestry'),
        ('veterinary', 'Veterinary Science')
    ]

class Student(models.Model):
    _name = 'student'
    _description = 'Student Information'
    _rec_name = 'full_name'
    
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age", compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", required=True)

    departments = fields.Selection([
        ('law', 'Faculty of Law'),
        ('medicine', 'Faculty of Medicine'),
        ('engineering', 'Faculty of Engineering'),
        ('arts', 'Faculty of Arts'),
        ('science', 'Faculty of Science'),
        ('economics', 'Faculty of Economics'),
        ('education', 'Faculty of Education'),
        ('social_sciences', 'Faculty of Social Sciences'),
        ('humanities', 'Faculty of Humanities'),
        ('agriculture', 'Faculty of Agriculture'),
    ], string="Faculty", required=True)

    trimester = fields.Selection([
                ('1', '1st Trimester'),
                ('2', '2nd Trimester'),
                ('3', '3rd Trimester'),
                ('4', '4th Trimester'),
                ('5', '5th Trimester'),
                ('6', '6th Trimester'),
                ('7', '7th Trimester'),
                ('8', '8th Trimester'),
                ('9', '9th Trimester'),
                ('10', '10th Trimester'),
                ('11', '11th Trimester'),
                ('12', '12th Trimester'),
            ], string="Trimester", required=True)
    career = fields.Selection(list_career, string="Career", required=True)

    active = fields.Boolean(string="Active", default=True)
    email = fields.Char(string="Email", required=True, help="Email address of the student.")
    # subject_ids = fields.Many2many('university.subject', string="Subjects", compute="_compute_subjects", readonly=False)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                record.age = today.year - record.date_of_birth.year - ((today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day))
            else:
                record.age = 0

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for student in self:
            student.full_name = f"{student.first_name} {student.last_name}"


class Professor(models.Model):
    _name = 'university.professor'
    _description = 'Professor'
    _rec_name = 'full_name'

    # Información básica del profesor
    first_name = fields.Char(string="Fist name")
    last_name = fields.Char(string="Last name")
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True)
    age = fields.Integer(string="Age")
    time_in_university = fields.Integer(string="Time at University (years)")
    is_tenured = fields.Boolean(string="Permanent", default=False)
    is_available = fields.Boolean(string="Available", default=True)
    current_courses = fields.Integer(string="Assigned Courses", compute="_compute_current_courses", store=True)
    max_courses = fields.Integer(string="Maximum Courses", default=3)
    subjects = fields.Many2many('university.subject', string="Materias")
    email = fields.Char(string="Email", required=True, help="Email address of the professor.")

    @api.depends('subjects')
    def _compute_current_courses(self):
        for professor in self:
            professor.current_courses = self.env['student.contract'].search_count(
                [('professor_ids', '=', professor.id)]
            )

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for student in self:
            student.full_name = f"{student.first_name} {student.last_name}"

class StudentContract(models.Model):
    _name = 'student.contract'
    _description = 'Student Contract'
    _rec_name = 'student_id'
    
    student_id = fields.Many2one('student', string="Student", required=True)
    subject_ids = fields.Many2many('university.subject', string="Subjects", required=True)
    professor_ids = fields.Many2many(
        'university.professor',
        string="Professors",
        domain="[('subjects', 'in', subject_ids), ('is_available', '=', True)]",
        required=True
    )
    price = fields.Float(string="Price", required=True)
    room = fields.Char(string="Salon/Course", required=True)    
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue')
    ], string="Payment Status", default='pending')

    creation_date = fields.Datetime(
                string="Creation Date",
                default=lambda self: datetime.now(),
                required=True
            )
    
    professor_hours = fields.Text(
        string="Professor Hours per Trimester",
        compute="_compute_professor_hours",
        store=True
    )

    @api.depends('professor_ids', 'subject_ids', 'subject_ids.hours_per_week', 'subject_ids.trimester_duration')
    def _compute_professor_hours(self):
        for record in self:
            professor_hours_dict = defaultdict(float)
            
            for subject in record.subject_ids:
                for professor in subject.professor_ids:
                    total_hours = subject.hours_per_week * subject.trimester_duration
                    if professor in record.professor_ids:
                        professor_hours_dict[professor.full_name] += total_hours
            
            # Format the result as a readable string
            record.professor_hours = "\n".join(
                f"{professor}: {hours:.2f} hours" for professor, hours in professor_hours_dict.items()
            )

    @api.model
    def create(self, vals):
        # student_id = vals.get('student_id')
        # trimester = vals.get('student_id').trimester  

        # existing_contract = self.env['student.contract'].search([
        #     ('student_id', '=', student_id),
        #     ('student_id.trimester', '=', trimester),
        # ], limit=1)

        # if existing_contract:
        #     return existing_contract

        if 'creation_date' not in vals:
            vals['creation_date'] = date.today()
        line = super(StudentContract, self).create(vals)

        if line.professor_ids:
            for professor in line.professor_ids:
                professor._compute_current_courses()
        return line

    def write(self, vals):
        res = super(StudentContract, self).write(vals)
        for line in self:
            if 'professor_ids' in vals:
                for professor in line.professor_ids:
                    professor._compute_current_courses()
        return res

    def unlink(self):
        professors = self.mapped('professor_ids')
        res = super(StudentContract, self).unlink()
        for professor in professors:
            professor._compute_current_courses()
        return res

    @api.constrains('professor_ids', 'subject_ids')
    def _check_professor_availability(self):
        for line in self:
            for professor in line.professor_ids:
                # Validar que el profesor no supere 3 cursos asignados
                if professor.current_courses >= professor.max_courses:
                    raise ValidationError(
                        f"El profesor {professor.name} ya tiene asignados el máximo de cursos permitidos (3)."
                    )
                
    @api.constrains('professor_ids', 'student_id')
    def _check_professor_availability_per_trimester(self):
        for line in self:
            trimester = line.student_id.trimester
            for professor in line.professor_ids:
                assigned_courses = self.env['student.contract'].search_count([
                    ('professor_ids', 'in', [professor.id]),
                    ('student_id.trimester', '=', trimester)
                ])
                if assigned_courses > 3:
                    raise ValidationError(
                        f"El profesor {professor.name} ya tiene asignados el máximo de cursos permitidos (3) para el trimestre {trimester}."
                    )

    @api.constrains('price')
    def _check_price(self):
        for line in self:
            if line.price < 0:
                raise ValidationError("El precio de una materia no puede ser negativo.")
            
class SubjectOption(models.Model):
    _name = 'university.subject.option'
    _description = 'Subject Option Information'

    name = fields.Char(string="Subject Name", required=True)
    code = fields.Char(string="Code", required=True)
    career_ids = fields.Many2many(
        'university.career',
        string="Careers",
        help="Careers that include this subject."
    )

class Subject(models.Model):
    _name = 'university.subject'
    _description = 'Subject Information'

    career_id = fields.Many2one('university.career', string="Career", required=True)
    trimester = fields.Selection([
                ('1', '1st Trimester'),
                ('2', '2nd Trimester'),
                ('3', '3rd Trimester'),
                ('4', '4th Trimester'),
                ('5', '5th Trimester'),
                ('6', '6th Trimester'),
                ('7', '7th Trimester'),
                ('8', '8th Trimester'),
                ('9', '9th Trimester'),
                ('10', '10th Trimester'),
                ('11', '11th Trimester'),
                ('12', '12th Trimester'),
            ], string="Trimester", required=True)
    name = fields.Many2one('university.subject.option', string="Subject", required=True)
    code = fields.Char(string="Code")
    hours_per_week = fields.Float(string="Hours per Week", required=True, default=4)
    trimester_duration = fields.Integer(string="Trimester Duration (weeks)", default=12)
    hours_per_trimester = fields.Float(
        string="Hours per Trimester",
        compute="_compute_trimester_hours",
        store=True
    )
    professor_ids = fields.Many2many('university.professor', string="professors")
    
    @api.depends('hours_per_week', 'trimester_duration')
    def _compute_trimester_hours(self):
        for record in self:
            record.hours_per_trimester = record.hours_per_week * record.trimester_duration

   
    @api.onchange('name')
    def _onchange_name(self):
        """
        Automatically set the code based on the selected subject.
        """
        _logger.info("Name value: %s", self.name) 
        if self.name and self.name.code:
            self.code = self.name.code
        else:
            self.code = False
    
    @api.model
    def create(self, values):
        """
        Override create to automatically set the code if not provided and avoid duplicate subjects.
        """
        
        if 'code' not in values and 'name' in values:
            values['code'] = values['name'].code
        return super(Subject, self).create(values)

    def assign_available_professors(self):
        """
        Automatically assign professors to the subject if none are assigned.
        """
        for subject in self:
            if not subject.professor_ids:
                professors = self.env['university.professor'].search([])
                subject.professor_ids = [(6, 0, professors.ids)]

    @api.onchange('career_id', 'trimester')
    def _onchange_career_trimester(self):
        """
        Filter the available subjects based on the degree and the selected term.
        """
        if self.career_id and self.trimester:
            career = self.career_id.name
            trimester = self.trimester
            available_subjects = CAREER_SUBJECTS.get(career, {}).get(trimester, [])
            subject_options = self.env['university.subject.option'].search([('name', 'in', available_subjects)])
            self.name = False
            return {'domain': {'name': [('id', 'in', subject_options.ids)]}}

class Career(models.Model):
    _name = 'university.career'
    _description = 'Career Information'

    name = fields.Selection(list_career, string="Career Name", required=True)
    department = fields.Selection([
        ('law', 'Faculty of Law'),
        ('medicine', 'Faculty of Medicine'),
        ('engineering', 'Faculty of Engineering'),
        ('arts', 'Faculty of Arts'),
        ('science', 'Faculty of Science'),
        ('economics', 'Faculty of Economics'),
        ('education', 'Faculty of Education'),
        ('social_sciences', 'Faculty of Social Sciences'),
        ('humanities', 'Faculty of Humanities'),
        ('agriculture', 'Faculty of Agriculture'),
    ], string="Faculty", required=True)

    code = fields.Char(string="Career Code", required=True, help="Unique code for the career.")
    duration_years = fields.Integer(string="Duration (Years)", required=True, help="Number of years to complete the career.")
    description = fields.Text(string="Description", help="Brief description of the career.")
    active = fields.Boolean(string="Active", default=True)

    subject_ids = fields.Many2many(
        'university.subject.option',
        'university_subject_option_career_rel',
        'career_id',
        'subject_id',
        string="Subjects",
        help="Subjects that are part of this career."
    )

    total_subjects = fields.Integer(
        string="Total Subjects",
        compute='_compute_total_subjects',
        store=True,
        help="Total number of subjects in the career."
    )

    @api.depends('subject_ids')
    def _compute_total_subjects(self):
        for record in self:
            record.total_subjects = len(record.subject_ids)

class Grade(models.Model):
    _name = 'university.grade'
    _description = 'Student Grades'

    student_id = fields.Many2one('student', string="Student", required=True)
    subject_id = fields.Many2one('subject', string="Subject", required=True)
    trimester = fields.Selection([
        ('1', '1st Trimester'),
        ('2', '2nd Trimester'),
        ('3', '3rd Trimester'),
        ('4', '4th Trimester'),
        ('5', '5th Trimester'),
        ('6', '6th Trimester'),
        ('7', '7th Trimester'),
        ('8', '8th Trimester'),
        ('9', '9th Trimester'),
        ('10', '10th Trimester'),
        ('11', '11th Trimester'),
        ('12', '12th Trimester'),
    ], string="Trimester", required=True)
    grade = fields.Float(string="Grade", required=True)
    professor_feedback = fields.Text(string="Professor Feedback")

class TrimesterSummary(models.Model):
    _name = 'university.trimester.summary'
    _description = 'Trimester Summary Information'

    student_id = fields.Many2one('student', string="Student", required=True)
    trimester = fields.Selection([
        ('1', '1st Trimester'),
        ('2', '2nd Trimester'),
        ('3', '3rd Trimester'),
        ('4', '4th Trimester'),
        ('5', '5th Trimester'),
        ('6', '6th Trimester'),
        ('7', '7th Trimester'),
        ('8', '8th Trimester'),
        ('9', '9th Trimester'),
        ('10', '10th Trimester'),
        ('11', '11th Trimester'),
        ('12', '12th Trimester'),
    ], string="Trimester", required=True)
    
    average_grade = fields.Float(string="Average Grade", compute="_compute_average_grade", store=True)
    professor_feedback_average = fields.Float(string="Professor Feedback Average", compute="_compute_professor_feedback_average", store=True)
    approved_subjects = fields.Integer(string="Approved Subjects", compute="_compute_approved_subjects", store=True)
    failed_subjects = fields.Integer(string="Failed Subjects", compute="_compute_failed_subjects", store=True)
    
    grade_ids = fields.One2many('university.grade', 'student_id', string="Grades")

    @api.depends('grade_ids.grade')
    def _compute_average_grade(self):
        for record in self:
            grades = record.grade_ids.filtered(lambda g: g.trimester == record.trimester)
            if grades:
                record.average_grade = sum(grades.mapped('grade')) / len(grades)
            else:
                record.average_grade = 0.0

    @api.depends('grade_ids.professor_feedback')
    def _compute_professor_feedback_average(self):
        for record in self:
            feedbacks = record.grade_ids.filtered(lambda g: g.trimester == record.trimester and g.professor_feedback)
            if feedbacks:
                feedback_lengths = sum(len(feedback.professor_feedback) for feedback in feedbacks)
                record.professor_feedback_average = feedback_lengths / len(feedbacks)
            else:
                record.professor_feedback_average = 0.0

    @api.depends('grade_ids.grade')
    def _compute_approved_subjects(self):
        for record in self:
            approved = sum(1 for grade in record.grade_ids if grade.trimester == record.trimester and grade.grade >= 6)
            record.approved_subjects = approved

    @api.depends('grade_ids.grade')
    def _compute_failed_subjects(self):
        for record in self:
            failed = sum(1 for grade in record.grade_ids if grade.trimester == record.trimester and grade.grade < 6)
            record.failed_subjects = failed


class ConsolidatedTable(models.Model):
    _name = 'consolidated.table'
    _description = 'Consolidated Table'
    _auto = False 

    student_id = fields.Many2one('student', string="Student")
    subject_id = fields.Many2one('university.subject', string="Subject")
    professor_id = fields.Many2one('university.professor', string="Professor")
    contract_id = fields.Many2one('student.contract', string="Contract")
    price = fields.Float(string="Price", readonly=True)
    room = fields.Char(string="Room", readonly=True)
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue')
    ], string="Payment Status", readonly=True)

    trimester = fields.Selection(
        related='contract_id.student_id.trimester', 
        string="Trimester", 
        readonly=True
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", readonly=True)
    departments = fields.Selection(
        related='contract_id.student_id.departments', 
        string="Faculty", 
        readonly=True
    )
    career = fields.Selection(
        related='contract_id.student_id.career',
        string="Career", 
        readonly=True
    )
    active = fields.Boolean(
                related='contract_id.student_id.active',
                string="Active",
                readonly=True
            )
    
     # Kpi variables
    total_contracts = fields.Integer(string="Total Contracts", compute='_compute_totals')
    total_payments = fields.Float(string="Total Payments", compute='_compute_totals')
    active_contracts = fields.Integer(
        string="Active Contracts",
        compute="_compute_active_contracts",
        readonly=True
    )

    total_professors = fields.Integer(string="Total Professors", compute='_compute_totals')

    @api.model
    def init(self):
        """
        Crea una vista SQL para unificar los datos de las tablas.
        """
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW consolidated_table AS (
                SELECT DISTINCT ON (sc.id)
                    sc.id AS id,
                    sc.student_id AS student_id,
                    ss.university_subject_id AS subject_id,
                    ps.university_professor_id AS professor_id,
                    sc.id AS contract_id,
                    sc.price AS price,
                    sc.room AS room,
                    sc.payment_status AS payment_status,
                    st.trimester AS trimester,
                    st.gender AS gender,
                    st.departments AS departments,
                    st.career AS career,
                    st.active AS active
                FROM student_contract sc
                -- Relación Many2many entre student_contract y university_subject
                JOIN student_contract_university_subject_rel ss ON ss.student_contract_id = sc.id
                -- Relación Many2many entre student_contract y university_professor
                JOIN student_contract_university_professor_rel ps ON ps.student_contract_id = sc.id
                -- Relación con la tabla student para obtener el trimestre, género y departamento
                JOIN student st ON st.id = sc.student_id
            )
        """)

    @api.model
    def get_dashboard_data(self):
        """Obtiene los datos necesarios para los gráficos."""
        gender_distribution = self._get_gender_distribution()
        payment_status = self._get_payment_status()
        departments = self._get_departments_distribution()
        subjects_by_student = self._get_subjects_by_student()
        subjects_by_professor = self._get_subjects_by_professor()
        contract_by_department = self._get_contracts_by_department()
        contract_by_career = self._get_contracts_by_career()

        return {
            'gender_distribution': gender_distribution,
            'payment_status': payment_status,
            'departments': departments,
            'subjects_by_student': subjects_by_student,
            'subjects_by_professor': subjects_by_professor,            
            'contract_by_department':contract_by_department,
            'contract_by_career':contract_by_career,
        }

    def _get_gender_distribution(self):
        """Calcula la distribución de género de manera manual."""
        gender_count = {'Male': 0, 'Female': 0, 'Other': 0}
        
        records = self.search([('gender', '!=', False)])
        
        for record in records:
            if record.gender == 'male':
                gender_count['Male'] += 1
            elif record.gender == 'female':
                gender_count['Female'] += 1
            else:
                gender_count['Other'] += 1
        
        return [{'label': gender, 'value': count} for gender, count in gender_count.items()]

    def _get_payment_status(self):
        """Calcula el estado de pago de manera manual."""
        status_count = {'Pending': 0, 'Paid': 0, 'Overdue': 0}
        
        records = self.search([('payment_status', '!=', False)])
        
        for record in records:
            if record.payment_status == 'pending':
                status_count['Pending'] += 1
            elif record.payment_status == 'paid':
                status_count['Paid'] += 1
            elif record.payment_status == 'overdue':
                status_count['Overdue'] += 1
        
        return [{'label': status, 'value': count} for status, count in status_count.items()]

    def _get_departments_distribution(self):
        department_count = {}
        
        records = self.env['student'].search([])

        for record in records:
            department = record.departments.capitalize()
            if department not in department_count:
                department_count[department] = 0
            department_count[department] += 1
        
        return [{'label': department, 'value': count} for department, count in department_count.items()]

    def _get_subjects_by_student(self):
        student_contracts = self.env['student.contract'].search([])
        subject_count = {}
        for contract in student_contracts:
            for subject in contract.subject_ids:
                subject_id = subject.id
                if subject_id not in subject_count:
                    subject_count[subject_id] = 0
                subject_count[subject_id] += 1

        subject_data = []
        for subject_id, count in subject_count.items():
            subject = self.env['university.subject'].browse(subject_id)
            subject_data.append({
                'label': subject.name.name.capitalize(),  
                'value': count 
            })

        subject_data.sort(key=lambda x: x['value'], reverse=True)
        return subject_data
    
    def _get_subjects_by_professor(self):

        professors = self.env['university.professor'].search([])
        professor_count = {}
        for professor in professors:
            subject_count = {}
            for subject in professor.subjects:
                subject_id = subject.id
                if subject_id not in subject_count:
                    subject_count[subject_id] = 0
                subject_count[subject_id] += 1
            
            professor_count[professor.full_name] = subject_count
        
        subject_data = []
        for professor, subject_count in professor_count.items():
            updated_subject_count = {}

            for subject_id, count in subject_count.items():
    
                subject = self.env['university.subject'].browse(subject_id)
                subject_name = subject.name.name
                updated_subject_count[subject_name] = count

            professor_count[professor] = updated_subject_count
               
        all_subjects = set()
        for subjects in professor_count.values():
            all_subjects.update(subjects.keys())

        data_for_js = []
        for professor, subjects in professor_count.items():
            professor_data = {"Professor": professor}
            for subject in all_subjects:
                professor_data[subject] = subjects.get(subject, 0) 
            data_for_js.append(professor_data)

        return data_for_js
    
    def _get_contracts_by_department(self):
        student_contracts = self.env['student.contract'].search([])

        student_count = {}
        for contract in student_contracts:
            for student in contract.student_id:
                student = student.id
                if student not in student_count:
                    student_count[student] = 0
                student_count[student] += 1

        student_contract_data = []
        for student, count in student_count.items():
            student = self.env['student'].browse(student)
            student_contract_data.append({
                'label': f"Faculty of {student.departments.capitalize()}",  
                'value': count 
            })
        
        student_contract_data = order_data(student_contract_data)
        return student_contract_data
    
    def _get_contracts_by_career(self):
        student_contracts = self.env['student.contract'].search([])

        student_count = {}
        for contract in student_contracts:
            for student in contract.student_id:
                student = student.id
                if student not in student_count:
                    student_count[student] = 0
                student_count[student] += 1

        student_contract_data = []
        for student, count in student_count.items():
            student = self.env['student'].browse(student)
            student_contract_data.append({
                'label': student.career.replace("_", " ").capitalize(),  
                'value': count 
            })

        student_contract_data = order_data(student_contract_data)
        return student_contract_data
    
    @api.depends('contract_id')
    def _compute_totals(self):
       
        for record in self:
            record.total_professors = self.env['university.professor'].search_count([])
            record.total_contracts = self.env['student.contract'].search_count([])
            record.total_payments = sum(self.env['student.contract'].search([]).mapped('price'))
            _logger.info(f"Pago: {record.total_payments}")

    @api.depends('professor_id')
    def _compute_totals(self):

        import pdb; pdb.set_trace()
        for record in self:

            professors = self.env['consolidated.table'].search([('professor_id', '!=', False)])
            unique_professors = len(set(professors.mapped('professor_id.id')))
            record.total_professors = unique_professors

    @api.model
    def default_get(self, fields_list):
       
        res = super(ConsolidatedTable, self).default_get(fields_list)
        res.update({
            'total_contracts': self.env['student.contract'].search_count([]),
            'total_payments': sum(self.env['student.contract'].search([]).mapped('price')),
        })
        return res
    
    @api.depends('contract_id')
    def _compute_active_contracts(self):
        for record in self:
            active_contracts_count = self.env['student.contract'].search_count([
                ('student_id.active', '=', True)
            ])
            record.active_contracts = active_contracts_count
            

def order_data(data):
    sums = defaultdict(int)

    for item in data:
        sums[item['label']] += item['value']

    sorted_sums = sorted(sums.items(), key=lambda x: x[1], reverse=True)
    data = [{'label': label, 'value': value} for label, value in sorted_sums]

    return data