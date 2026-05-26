import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr_hospital.disease.report.wizard'
    _description = 'Звіт по хворобах за місяць'

    doctor_ids = fields.Many2many(
        comodel_name='hr_hospital.doctor',
        string='Лікарі',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr_hospital.disease',
        string='Хвороби',
    )
    date_from = fields.Date(string='Дата з', required=True,
                            default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(string='Дата по', required=True,
                          default=fields.Date.today)

    def action_generate_report(self):
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        if self.date_from:
            domain.append(('visit_date', '>=', str(self.date_from) + ' 00:00:00'))
        if self.date_to:
            domain.append(('visit_date', '<=', str(self.date_to) + ' 23:59:59'))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Звіт по хворобах',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {'group_by': ['disease_id']},
            'target': 'current',
        }
