import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Хвороба'
    _parent_name = 'parent_id'
    _parent_store = True

    name = fields.Char(string='Назва', required=True)
    code = fields.Char(string='Код')
    description = fields.Text(string='Опис')
    color = fields.Integer(string='Колір', default=0)
    parent_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Батьківська хвороба',
        ondelete='restrict',
        index=True,
    )
    child_ids = fields.One2many(
        comodel_name='hr_hospital.disease',
        inverse_name='parent_id',
        string='Дочірні хвороби',
    )
    parent_path = fields.Char(index=True, unaccent=False)
    active = fields.Boolean(string='Активний', default=True)

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if not self._check_recursion():
            raise ValidationError('Хвороба не може бути батьком самої себе (циклічність неприпустима).')

    def _compute_display_name(self):
        for rec in self:
            names = []
            current = rec
            visited = set()
            while current and current.id not in visited:
                visited.add(current.id)
                names.append(current.name or '')
                current = current.parent_id
            rec.display_name = ' / '.join(reversed(names))
