"""
Tests for the hr_hospital module (Block 3 model methods).

Covers:
- Doctor._compute_is_intern
- Doctor._compute_is_mentor
- Doctor._check_mentor_not_intern
- Visit.write  (protected fields on a done visit)
- Visit.unlink (cannot delete a done visit)
- Disease._check_parent_recursion
"""

from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase


def _assert_recursion_blocked(test_case, callable_):
    """Assert that callable_ raises UserError or ValidationError.

    Odoo's custom assertRaises does not accept a tuple of exception types,
    so we use a plain try/except instead.
    When _parent_store=True, _parent_store_update raises UserError before
    @api.constrains fires; both outcomes mean recursion was correctly blocked.
    """
    try:
        callable_()
    except (UserError, ValidationError):
        return
    test_case.fail("Expected UserError or ValidationError, but no exception was raised.")


class TestDoctorModel(TransactionCase):
    """Tests for hr_hospital.doctor model methods."""

    @classmethod
    def setUpClass(cls):
        """Create shared test data for all doctor tests."""
        super().setUpClass()
        cls.category_intern = cls.env.ref(
            'hr_hospital.category_intern', raise_if_not_found=False
        )
        cls.category_specialist = cls.env.ref(
            'hr_hospital.category_specialist', raise_if_not_found=False
        )
        cls.doctor = cls.env['hr_hospital.doctor'].create({'name': 'Тест Лікар'})
        cls.intern = cls.env['hr_hospital.doctor'].create({
            'name': 'Тест Інтерн',
            'category_id': cls.category_intern.id if cls.category_intern else False,
        })

    def test_compute_is_intern_true(self):
        """Doctor with intern category must have is_intern = True."""
        if not self.category_intern:
            self.skipTest('category_intern fixture not found')
        self.assertTrue(
            self.intern.is_intern,
            'Лікар з категорією «Лікар-інтерн» повинен мати is_intern = True',
        )

    def test_compute_is_intern_false(self):
        """Doctor without intern category must have is_intern = False."""
        if not self.category_specialist:
            self.skipTest('category_specialist fixture not found')
        self.doctor.category_id = self.category_specialist
        self.assertFalse(
            self.doctor.is_intern,
            'Лікар зі спеціалістичною категорією повинен мати is_intern = False',
        )

    def test_compute_is_mentor(self):
        """Doctor becomes a mentor when an intern is linked to them."""
        self.intern.mentor_id = self.doctor
        self.doctor._compute_is_mentor()
        self.assertTrue(
            self.doctor.is_mentor,
            'Лікар, якому призначено інтерна, повинен мати is_mentor = True',
        )

    def test_compute_is_mentor_no_interns(self):
        """Doctor without interns must have is_mentor = False."""
        doctor = self.env['hr_hospital.doctor'].create({'name': 'Без інтернів'})
        self.assertFalse(
            doctor.is_mentor,
            'Лікар без інтернів повинен мати is_mentor = False',
        )

    def test_check_mentor_not_intern_raises(self):
        """Setting an intern as mentor of another doctor must raise ValidationError."""
        if not self.category_intern:
            self.skipTest('category_intern fixture not found')
        doctor2 = self.env['hr_hospital.doctor'].create({'name': 'Лікар 2'})
        with self.assertRaises(ValidationError):
            doctor2.mentor_id = self.intern


class TestVisitModel(TransactionCase):
    """Tests for hr_hospital.visit model methods."""

    @classmethod
    def setUpClass(cls):
        """Create shared test data for all visit tests."""
        super().setUpClass()
        cls.doctor = cls.env['hr_hospital.doctor'].create({'name': 'Лікар для візиту'})
        cls.doctor2 = cls.env['hr_hospital.doctor'].create({'name': 'Інший лікар'})
        cls.patient = cls.env['hr_hospital.patient'].create({'name': 'Пацієнт для візиту'})
        cls.visit_done = cls.env['hr_hospital.visit'].create({
            'doctor_id': cls.doctor.id,
            'patient_id': cls.patient.id,
            'state': 'done',
        })
        cls.visit_planned = cls.env['hr_hospital.visit'].create({
            'doctor_id': cls.doctor.id,
            'patient_id': cls.patient.id,
            'state': 'planned',
        })

    def test_write_done_visit_doctor_raises(self):
        """Changing doctor_id on a done visit must raise UserError."""
        with self.assertRaises(UserError):
            self.visit_done.write({'doctor_id': self.doctor2.id})

    def test_write_planned_visit_allowed(self):
        """Changing doctor_id on a planned visit must succeed."""
        self.visit_planned.write({'doctor_id': self.doctor2.id})
        self.assertEqual(
            self.visit_planned.doctor_id, self.doctor2,
            'Зміна лікаря запланованого візиту повинна бути дозволена',
        )

    def test_unlink_done_visit_raises(self):
        """Deleting a done visit must raise UserError."""
        visit = self.env['hr_hospital.visit'].create({
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'state': 'done',
        })
        with self.assertRaises(UserError):
            visit.unlink()

    def test_unlink_planned_visit_allowed(self):
        """Deleting a planned visit must succeed."""
        visit = self.env['hr_hospital.visit'].create({
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'state': 'planned',
        })
        self.assertTrue(visit.unlink(), 'Видалення запланованого візиту повинно бути дозволено')


class TestDiseaseModel(TransactionCase):
    """Tests for hr_hospital.disease model methods."""

    @classmethod
    def setUpClass(cls):
        """Create shared test data for all disease tests."""
        super().setUpClass()
        cls.disease_a = cls.env['hr_hospital.disease'].create({'name': 'Хвороба А'})
        cls.disease_b = cls.env['hr_hospital.disease'].create({
            'name': 'Хвороба Б',
            'parent_id': cls.disease_a.id,
        })

    def test_check_parent_recursion_self(self):
        """Setting a disease as its own parent must be blocked (UserError or ValidationError)."""
        _assert_recursion_blocked(self, lambda: setattr(self.disease_a, 'parent_id', self.disease_a))

    def test_check_parent_recursion_cycle(self):
        """Creating a circular parent chain must be blocked (UserError or ValidationError)."""
        _assert_recursion_blocked(self, lambda: setattr(self.disease_a, 'parent_id', self.disease_b))

    def test_compute_display_name_with_parent(self):
        """Disease with parent must include parent name in display_name."""
        self.assertIn(
            self.disease_a.name,
            self.disease_b.display_name,
            'display_name дочірньої хвороби повинен містити назву батьківської',
        )

    def test_compute_display_name_root(self):
        """Root disease display_name must equal its own name."""
        self.assertEqual(
            self.disease_a.display_name,
            self.disease_a.name,
            'display_name кореневої хвороби повинен збігатися з її назвою',
        )
