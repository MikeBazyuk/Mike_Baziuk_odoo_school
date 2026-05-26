import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class MedicInfo(models.AbstractModel):
    _name = 'hospital.medic.info'
    _description = 'Медична інформація'

    blood_group = fields.Selection(
        [
            ('o_pos', 'O(I) Rh+'),
            ('o_neg', 'O(I) Rh-'),
            ('a_pos', 'A(II) Rh+'),
            ('a_neg', 'A(II) Rh-'),
            ('b_pos', 'B(III) Rh+'),
            ('b_neg', 'B(III) Rh-'),
            ('ab_pos', 'AB(IV) Rh+'),
            ('ab_neg', 'AB(IV) Rh-'),
        ],
        string='Група крові',
    )
    gender = fields.Selection(
        [
            ('male', 'Чоловік'),
            ('female', 'Жінка'),
        ],
        string='Стать',
    )
    birth_date = fields.Date(string='Дата народження')
    age = fields.Integer(string='Вік', compute='_compute_age')

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(today, rec.birth_date).years
            else:
                rec.age = 0
