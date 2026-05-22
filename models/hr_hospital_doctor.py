import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Name', required=True)
    specialty = fields.Char(string='Specialty')
    active = fields.Boolean(default=True)
