{
    'name': 'HR Hospital',
    'summary': "Education project of hospital managment system",
    'author': 'Mykhailo Baziuk',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '19.0.2.1.0',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/ir.model.access.csv',
        'data/hr_hospital_sequence_data.xml',
        'data/hr_hospital_disease_data.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'views/hr_hospital_menu.xml',
    ],
    'demo': [
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

}