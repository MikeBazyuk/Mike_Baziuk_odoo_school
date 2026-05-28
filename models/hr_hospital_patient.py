import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    """Модель пацієнта лікарні.

    Зберігає персональні дані пацієнта, його страховий поліс,
    персонального лікаря та зв'язаного користувача системи.
    """

    _name = 'hr_hospital.patient'
    _inherit = ['hospital.medic.info']
    _description = 'Пацієнт'

    name = fields.Char(string='ПІБ', required=True)
    phone = fields.Char(string='Телефон')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Користувач системи',
        help='Пов\'язаний користувач Odoo. Використовується для обмеження доступу до власних відвідувань.',
    )
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
    visit_count = fields.Integer(
        string='Кількість візитів',
        compute='_compute_visit_count',
    )
    active = fields.Boolean(string='Активний', default=True)

    def _compute_visit_count(self):
        """Підраховує загальну кількість відвідувань пацієнта."""
        for patient in self:
            patient.visit_count = self.env['hr_hospital.visit'].search_count([
                ('patient_id', '=', patient.id),
            ])

    def action_show_visits(self):
        """Відкриває список відвідувань поточного пацієнта."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Візити: {self.name}',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }

    def action_create_visit(self):
        """Відкриває форму створення нового відвідування для поточного пацієнта."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Новий візит',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.personal_doctor_id.id,
            },
        }
