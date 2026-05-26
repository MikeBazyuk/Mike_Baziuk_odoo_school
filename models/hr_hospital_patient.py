import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _inherit = ['hospital.medic.info']
    _description = 'Пацієнт'

    name = fields.Char(string='ПІБ', required=True)
    phone = fields.Char(string='Телефон')
    personal_doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Персональний лікар',
    )
    doctor_history_ids = fields.One2many(
        comodel_name='hospital.doctor.history',
        inverse_name='patient_id',
        string='Історія персональних лікарів',
    )
    insurance_number = fields.Char(string='Номер страхового поліса', size=20)
    active = fields.Boolean(string='Активний', default=True)
