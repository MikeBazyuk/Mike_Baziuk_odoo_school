import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'

    name = fields.Char(string='Name', required=True)
    birth_date = fields.Date(string='Date of Birth')
    phone = fields.Char(string='Phone')
    personal_doctor_id = fields.Many2one('hr_hospital.doctor', string='Personal Doctor')
    active = fields.Boolean(default=True)
