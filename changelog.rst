=========
Changelog
=========

`19.0.2.5.0`
-------------

*Released: 2024-05-28*

**Block 6 – Security, Translations, Tests, Documentation**

* [ADD] Five security groups with inheritance chain:
  Patient → Intern → Doctor → Manager → Administrator
* [ADD] Record rules for ``hr_hospital.visit``:
  patient sees own, intern edits own, doctor edits own + interns,
  manager reads all, admin full CRUD
* [ADD] ``user_id`` field on ``hr_hospital.patient`` for record-rule binding
* [ADD] Ukrainian translation file ``i18n/uk.po`` (models, fields, selections,
  groups, menu items, disease classifier labels)
* [ADD] Unit tests in ``tests/test_hr_hospital.py`` covering 7 model methods
* [ADD] Module description ``static/description/index.html``
* [ADD] ``README.rst`` with installation and configuration instructions
* [ADD] ``changelog.rst``
* [ADD] Docstrings on all model classes and public methods

`19.0.2.4.0`
-------------

*Block 5 – Reports*

* [ADD] QWeb report action for Doctor (HTML, A4 portrait)
* [ADD] Full report: company header, doctor info, visit history (colour-coded
  by status), patient list, footer with print date and city
* [ADD] Custom paperformat ``hr_hospital_doctor_paperformat``
* [ADD] Sub-templates: company, info, visits, patients, footer

`19.0.2.3.0`
-------------

*Block 4 – Wizards & Advanced Views*

* [ADD] Wizard: mass reassign doctor for patients
* [ADD] Wizard: visit report by doctor
* [ADD] Wizard: disease report
* [ADD] Calendar, pivot, graph views for visits
* [ADD] Search panel on visits

`19.0.2.2.0`
-------------

*Block 3 – Core Models*

* [ADD] Models: ``hr_hospital.doctor``, ``hr_hospital.patient``,
  ``hr_hospital.visit``, ``hr_hospital.disease``,
  ``hospital.doctor.category``, ``hospital.doctor.history``
* [ADD] Abstract model ``hospital.medic.info`` (blood group, gender, DOB, age)
* [ADD] Computed fields: ``is_intern``, ``is_mentor``, ``visit_count``,
  ``disease_visit_count``, ``age``
* [ADD] Constraints: mentor cannot be intern, no circular disease parents
* [ADD] Form, list, kanban, search views for all models

`19.0.1.0.0`
-------------

*Block 1–2 – Module scaffold*

* [ADD] Initial module structure
* [ADD] Manifest, security CSV, demo data
