import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Масове перевизначення персонального лікаря'

    new_doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Новий лікар',
        required=True,
    )
    change_date = fields.Date(
        string='Дата зміни',
        default=fields.Date.today,
    )

    def action_reassign(self):
        active_ids = self._context.get('active_ids', [])
        patients = self.env['hr_hospital.patient'].browse(active_ids)
        for patient in patients:
            active_histories = self.env['hospital.doctor.history'].search(
                [
                    ('patient_id', '=', patient.id),
                    ('active', '=', True),
                ]
            )
            active_histories.write(
                {
                    'change_date': self.change_date,
                    'active': False,
                }
            )
            self.env['hospital.doctor.history'].create(
                {
                    'patient_id': patient.id,
                    'doctor_id': self.new_doctor_id.id,
                    'appointment_date': self.change_date,
                }
            )
            patient.personal_doctor_id = self.new_doctor_id
        return {'type': 'ir.actions.act_window_close'}
