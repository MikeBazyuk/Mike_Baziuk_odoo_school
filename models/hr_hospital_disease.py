import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    name = fields.Char(
        string='Name',
        required=True
    )

    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
