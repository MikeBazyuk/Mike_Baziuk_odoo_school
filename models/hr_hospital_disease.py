import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Disease(models.Model):
    """Ієрархічний класифікатор хвороб.

    Підтримує деревоподібну структуру (parent_id / child_ids) та
    формує повний шлях назви хвороби через ``_compute_display_name``.
    Захищає від циклічних посилань через ``_check_parent_recursion``.
    """

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
    parent_path = fields.Char(index=True)
    active = fields.Boolean(string='Активний', default=True)

    # Must be re-declared with recursive=True because the compute depends on
    # parent_id.display_name, which is the field itself — an inherently recursive chain.
    display_name = fields.Char(
        compute='_compute_display_name',
        recursive=True,
        store=False,
    )

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        """Перевіряє відсутність циклічних зв'язків у ієрархії хвороб.

        :raises ValidationError: якщо встановлення ``parent_id`` створює цикл.
        """
        if self._has_cycle():
            raise ValidationError("Хвороба не може бути батьком самої себе (циклічність неприпустима).")

    @api.depends('name', 'parent_id.display_name')
    def _compute_display_name(self):
        """Формує повний шлях назви хвороби через « / » від кореня до поточного вузла."""
        for rec in self:
            names = []
            current = rec
            visited = set()
            while current and current.id not in visited:
                visited.add(current.id)
                names.append(current.name or '')
                current = current.parent_id
            rec.display_name = ' / '.join(reversed(names))
