import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Візит пацієнта'

    state = fields.Selection(
        [
            ('planned', 'Заплановано'),
            ('done', 'Завершено'),
            ('cancelled', 'Скасовано'),
        ],
        string='Статус',
        default='planned',
        required=True,
    )
    scheduled_date = fields.Datetime(string='Запланована дата')
    visit_date = fields.Datetime(string='Дата візиту')
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Лікар',
        required=True,
    )
    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        string='Пацієнт',
        required=True,
    )
    disease_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Хвороба',
    )
    disease_visit_count = fields.Integer(
        string='Візити з цією хворобою',
        compute='_compute_disease_visit_count',
    )
    summary = fields.Html(string='Епікриз')
    recommendations = fields.Text(string='Рекомендації')
    active = fields.Boolean(string='Активний', default=True)

    def _compute_disease_visit_count(self):
        for rec in self:
            if rec.disease_id:
                rec.disease_visit_count = self.search_count(
                    [
                        ('disease_id', '=', rec.disease_id.id),
                    ]
                )
            else:
                rec.disease_visit_count = 0

    def action_related_disease_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Візити: {self.disease_id.display_name}',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list,form',
            'domain': [('disease_id', '=', self.disease_id.id)],
            'target': 'current',
        }

    def write(self, vals):
        protected = {'visit_date', 'scheduled_date', 'doctor_id'}
        for rec in self:
            if rec.state == 'done' and protected & set(vals):
                raise UserError(_('Неможливо змінити дату/час або лікаря завершеного візиту.'))
        if vals.get('active') is False:
            for rec in self:
                if rec.state == 'done':
                    raise UserError(_('Неможливо архівувати завершений візит.'))
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise UserError(_('Неможливо видалити завершений візит.'))
        return super().unlink()
