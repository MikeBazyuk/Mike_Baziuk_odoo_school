from odoo import fields, models


class DoctorCategory(models.Model):
    _name = 'hospital.doctor.category'
    _description = 'Кваліфікація лікарів'
    _order = 'sequence, name'

    name = fields.Char(string='Назва', required=True)
    sequence = fields.Integer(string='Послідовність', default=10)
    doctor_ids = fields.One2many(
        comodel_name='hr_hospital.doctor',
        inverse_name='category_id',
        string='Лікарі',
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Назва кваліфікації має бути унікальною!'),
    ]
