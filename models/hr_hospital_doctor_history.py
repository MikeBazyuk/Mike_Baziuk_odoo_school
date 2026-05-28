import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class DoctorHistory(models.Model):
    """Журнал зміни персональних лікарів пацієнта.

    Кожен запис фіксує дату призначення та дату зміни лікаря для конкретного
    пацієнта. Попереджає, якщо дата зміни раніша за дату призначення.
    """

    _name = 'hospital.doctor.history'
    _description = 'Історія персональних лікарів'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        string='Пацієнт',
        required=True,
        ondelete='cascade',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Лікар',
        required=True,
        ondelete='restrict',
    )
    appointment_date = fields.Date(
        string='Дата призначення', required=True, default=fields.Date.today,
    )
    change_date = fields.Date(string='Дата зміни лікаря')
    active = fields.Boolean(string='Активний', default=True)

    @api.onchange('change_date', 'appointment_date')
    def _onchange_dates(self):
        """Попереджає, якщо дата зміни лікаря раніша за дату призначення."""
        if self.change_date and self.appointment_date and self.change_date < self.appointment_date:
            return {
                'warning': {
                    'title': 'Помилка дати',
                    'message': 'Дата зміни лікаря не може бути раніше ніж дата призначення',
                }
            }
        return None

    @api.depends('patient_id.name', 'doctor_id.name', 'doctor_id.category_id.name', 'appointment_date')
    def _compute_display_name(self):
        """Формує відображувану назву: «Пацієнт - Лікар (категорія) дата»."""
        for rec in self:
            patient = rec.patient_id.name or ''
            doctor = rec.doctor_id.name or ''
            category = rec.doctor_id.category_id.name
            cat_str = f' ({category})' if category else ''
            date_str = str(rec.appointment_date) if rec.appointment_date else ''
            rec.display_name = f'{patient} - {doctor}{cat_str} {date_str}'.strip()
