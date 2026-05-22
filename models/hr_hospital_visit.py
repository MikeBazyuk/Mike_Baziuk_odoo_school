import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'

    visit_date = fields.Datetime(string='Visit Date', default=fields.Datetime.now, required=True)
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hr_hospital.patient', string='Patient', required=True)
    disease_ids = fields.Many2many('hr_hospital.disease', string='Diseases')
    recommendations = fields.Text(string='Recommendations')
    active = fields.Boolean(default=True)
