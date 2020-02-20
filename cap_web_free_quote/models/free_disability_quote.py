# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

from odoo import models, fields, api


class FreeDisabilityQuote(models.Model):
    _name = 'free.disability.quote'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Free Disability Quote'

    name = fields.Char(string="Log")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done')
    ], string="Status", default="draft", track_visibility="onchange")

    # Step - 1
    question_1 = fields.Char(string="First Name",
                             track_visibility="onchange")
    question_2 = fields.Char(string="Last Name",
                             track_visibility="onchange")
    question_3 = fields.Char(string="Email",
                             track_visibility="onchange")
    question_4 = fields.Char(string="Phone")
    question_5 = fields.Char(string="Area Code")

    # Step - 2
    question_6 = fields.Char(string="Medical Speciality")
    question_7 = fields.Date(string="Date of Birth")
    question_8 = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
    ], string="Sex")
    question_9 = fields.Char(string="State")

    # Step - 3
    question_10 = fields.Char(string="Desired Monthly Benefit")
    question_11 = fields.Selection([
        ('True Own Occupation', 'True Own Occupation'),
        ('Modified Own Occupation', 'Modified Own Occupation'),
    ], string="Definition of Total Disability")
    question_12 = fields.Selection([
        ('90 Days', '90 Days'),
        ('180 Days', '180 Days'),
        ('365 Days', '365 Days')
    ], string="Waiting/Elimination Period")
    question_13 = fields.Selection([
        ('Age 65', 'Age 65'),
        ('Age 67', 'Age 67'),
        ('Age 70', 'Age 70'),
    ], string="Benefit Period")

    # Step - 4
    question_14 = fields.Selection([
        ('Residual Disability Benefits', 'Residual Disability Benefits'),
        ('None', 'None'),
    ], string="Residual/Partial Coverage")
    question_15 = fields.Selection([
        ('3% COLA', '3% COLA'),
        ('6% COLA', '6% COLA'),
        ('None', 'None'),
    ], string="Benefit Period")
    question_16 = fields.Selection([
        ('Non-Cancellable', 'Non-Cancellable'),
        ('Guaranteed Renewable', 'Guaranteed Renewable'),
    ], string="Guarantee")
    question_17 = fields.Selection([
        ('24 Month Limitation', '24 Month Limitation'),
        ('Unlimited', 'Unlimited'),
    ], string="Mental/Nervous Limitation")
    question_18 = fields.Char(string="Hospital Affiliation")

    @api.multi
    def send_form_mail(self):
        template = self.env.ref(
            'cap_web_free_quote.mail_free_disability_form',
            raise_if_not_found=False)
        template.send_mail(self.id)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'free.disability.quote')
        return super(FreeDisabilityQuote, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(FreeDisabilityQuote, self).write(vals)
        if vals.get('state', '') == 'done':
            self.send_form_mail()
        return res
