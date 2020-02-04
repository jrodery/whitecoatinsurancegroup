# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

from odoo import models, fields, api, _


class LifeInsuranceEstimate(models.Model):
    _name = 'life.insurance.estimate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Life Insurance Estimate Form'

    select_boolean = [('Yes', 'Yes'), ('No', 'No')]

    name = fields.Char(string="Log")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done')
    ], string="Status", default="draft", track_visibility="onchange")


    # Step - 1
    question_28 = fields.Char(string="What is your First Name?")
    question_29 = fields.Char(string="What is your Last Name?")
    question_30 = fields.Char(string="Where can we email your report to?")
    question_31 = fields.Char(string="Whats your best contact phone number?")

    # Step - 2
    question_1 = fields.Integer(string="Your Current Age?")
    question_2 = fields.Integer(string="Your Desired Retirement Age?")
    remaining_age = fields.Integer(string="Years Until Retirement")
    question_3 = fields.Selection(select_boolean,
                                  string="Does your spouse work?")
    question_4 = fields.Integer(
        string="How much income does your spouse earn per year?")
    question_5 = fields.Selection(
        select_boolean, string="Will your spouse continue to work "
                               "if you passed away?")

    # Step - 3
    question_6 = fields.Selection(
        select_boolean,
        string="Do you currently have or plan to have children?")
    question_7 = fields.Integer(
        string="If yes, How many do you have or plan to have?")
    question_8 = fields.Integer(string="Age of your youngest child?")
    question_9 = fields.Selection(
        select_boolean, string="Will your untimely death result in added child"
                               " care expense?")
    question_10 = fields.Char(
        string="If Yes, How much per year to you anticipate you’d have to add "
               "to your annual budget to cover for child care?")

    # Step - 4
    question_11 = fields.Selection(
        select_boolean, string="Do you plan on paying for college?")
    question_12 = fields.Char(
        string="If Yes, by the time your child reaches collage - how much do "
               "you think it will cost to send each individual child through "
               "school?")
    question_13 = fields.Selection(
        select_boolean, string="Do you currently have any money saved "
                               "for college?")
    question_14 = fields.Float(string="If yes, what is the approx balance of "
                                      "your college savings?")

    # Step - 5
    question_15 = fields.Selection(select_boolean,
                                   string="Do you have have a mortgage?")
    question_16 = fields.Float(
        string="If Yes, What is your mortgage balance?")
    question_17 = fields.Selection(
        select_boolean, string="Do you own money on credit cards?")
    question_18 = fields.Float(
        string="If Yes What is your credit Card Balance?")
    question_19 = fields.Selection(select_boolean,
                                   string="Do you have car payments?")
    question_20 = fields.Float(
        string="If yes what are your car payments balances?")
    question_21 = fields.Selection(
        select_boolean, string="Do you have any additional Debt (student loans,"
                               " personal loans, etc.)")
    question_22 = fields.Float(
        string="If Yes, What is the total balance you owe?")

    # Step - 6
    question_23 = fields.Float(
        string="If you own your own home what are your annual property taxes? "
               "If you rent, what is your monthly rent?")
    question_24 = fields.Float(string="What is the cost of your Homeowners or "
                                      "renters insurance policy annually?")
    question_25 = fields.Selection(
        select_boolean, string="Are you responsible for paying HOA fees?")
    question_26 = fields.Float(
        string="If yes, what is your monthly HOA amount?")
    question_27 = fields.Float(
        string="Excluding your Mortgage Payment, Credit Card Payments, Car "
               "Payments, or the cost of any additional debt, how much per "
               "month do you spend on additional living expenses (Food, Fuel, "
               "Electricity, Gas, Private School, Entertainment, Landscaping, "
               "Cleaning services, etc)?")

    @api.constrains('question_1', 'question_2')
    def _check_age(self):
        for res in self:
            if res.question_1 > res.question_2:
                raise ValueError(_('Please add valid age.'))

    @api.onchange('question_1', 'question_2')
    def _onchange_age(self):
        for res in self:
            if res.question_1 and res.question_2:
                res.remaining_age = res.question_2 - res.question_1

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'life.insurance.estimate')
        return super(LifeInsuranceEstimate, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(LifeInsuranceEstimate, self).write(vals)
        if vals.get('state', '') == 'done':
            self.send_estimation_mail()
        return res

    @api.multi
    def send_estimation_mail(self):
        template = self.env.ref(
            'cap_web_free_quote.mail_life_insurance_estimate_form',
            raise_if_not_found=False)
        template.send_mail(self.id)
