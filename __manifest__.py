{
    'name': 'HR Hospital',
    'summary': "Навчальний модуль управління лікарнею",
    'author': 'Mykhailo Baziuk',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '19.0.2.5.0',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/hr_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_hospital_rules.xml',

        'data/hr_hospital_sequence_data.xml',
        'data/hr_hospital_doctor_category_data.xml',
        'data/hr_hospital_disease_data.xml',

        'views/hr_hospital_doctor_category_views.xml',
        'views/hr_hospital_doctor_history_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_menu.xml',

        'wizard/hr_hospital_visit_report_wizard_view.xml',
        'wizard/hr_hospital_mass_rassign_doctor_wizard_view.xml',
        'wizard/hr_hospital_disease_report_wizard_view.xml',

        'report/hr_hospital_doctor_report.xml',
    ],
    'demo': [
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_disease_demo.xml',
        'demo/hr_hospital_doctor_history_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

}
