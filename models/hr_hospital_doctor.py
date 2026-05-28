import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Doctor(models.Model):

    _name = 'hr_hospital.doctor'
    _inherit = ['hospital.medic.info']
    _description = 'Лікар'

    name = fields.Char(string='ПІБ', required=True)
    specialty = fields.Char(string='Спеціальність')
    category_id = fields.Many2one(
        comodel_name='hospital.doctor.category',
        string='Кваліфікація',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Користувач системи',
    )
    is_intern = fields.Boolean(
        string='Лікар є інтерном',
        compute='_compute_is_intern',
        store=True,
    )
    is_mentor = fields.Boolean(
        string='Є ментором',
        compute='_compute_is_mentor',
        store=True,
    )
    mentor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Ментор',
        domain="[('is_intern', '=', False)]",
    )
    intern_ids = fields.One2many(
        comodel_name='hr_hospital.doctor',
        inverse_name='mentor_id',
        string='Інтерни',
    )
    active = fields.Boolean(string='Активний', default=True)

    @api.depends('category_id')
    def _compute_is_intern(self):

        intern_cat = self.env.ref('hr_hospital.category_intern', raise_if_not_found=False)
        for doctor in self:
            doctor.is_intern = bool(intern_cat and doctor.category_id == intern_cat)

    @api.depends('intern_ids')
    def _compute_is_mentor(self):
        for doctor in self:
            doctor.is_mentor = bool(doctor.intern_ids)

    @api.constrains('mentor_id')
    def _check_mentor_not_intern(self):
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError("Ментором не може бути лікар-інтерн.")
