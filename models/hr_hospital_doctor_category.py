import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class DoctorCategory(models.Model):
    """Довідник кваліфікацій лікарів.

    Визначає рівень кваліфікації (інтерн, спеціаліст, лікар вищої категорії
    тощо). Використовується для обчислення поля ``is_intern`` у моделі лікаря.
    """

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

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'Назва кваліфікації має бути унікальною!',
    )
