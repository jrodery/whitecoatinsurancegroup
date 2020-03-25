# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

import uuid

from odoo import models, fields, api, _


class LifeInsuranceEstimate(models.Model):
    _name = 'life.insurance.estimate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Life Insurance Estimate Form'

    select_boolean = [('Yes', 'Yes'), ('No', 'No')]

    ref_code = fields.Char(string="Reference", default=uuid.uuid4())
    name = fields.Char(string="Log")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ('requested_quote', 'Requested Quote')
    ], string="Status", default="draft", track_visibility="onchange")

    # Step - 1
    question_28 = fields.Char(string="What is your First Name?",
                              track_visibility="onchange")
    question_29 = fields.Char(string="What is your Last Name?",
                              track_visibility="onchange")
    question_30 = fields.Char(string="Where can we email your report to?",
                              track_visibility="onchange")
    question_31 = fields.Char(string="Whats your best contact phone number?",
                              track_visibility="onchange")
    question_32 = fields.Char(string="What is the zip code of your area?",
                              track_visibility="onchange")

    # Step - 2
    question_1 = fields.Integer(string="Your Current Age?")
    question_2 = fields.Integer(string="Your Desired Retirement Age?")
    remaining_age = fields.Integer(store="True", compute="_compute_age",
                                   string="Years Until Retirement")
    question_3 = fields.Selection(select_boolean,
                                  string="Does your spouse work?")
    question_4 = fields.Float(
        string="How much income does your spouse earn per year?")
    question_5 = fields.Selection(
        select_boolean,
        string="Will your spouse continue to work if you passed away?")
    question_5_1 = fields.Selection(
        select_boolean,
        string="If yes, will you have an added child care expense?")
    question_5_2 = fields.Float(
        string="If you die, how much do you anticipate the annual child expense to be? "
               "would add to your budget")
    question_5_3 = fields.Float(
        store="True", compute="_compute_spouse_income",
        string="Spouses income minus Additional child care expense")
    question_5_4 = fields.Float(
        store="True", compute="_compute_spouse_income",
        string="Spouses potential pre tax career earnings")

    @api.onchange('question_5_1')
    def _onchange_question_5_1(self):
        if self.question_5_1 == "No":
            self.question_5_2 = 0.0

    @api.depends('question_4', 'question_5_2', 'remaining_age')
    def _compute_spouse_income(self):
        remains = self.question_4 - self.question_5_2
        self.question_5_3 = remains
        self.question_5_4 = remains * self.remaining_age

    # Step - 3
    question_6 = fields.Selection(
        select_boolean,
        string="Do you currently have or plan to have children?")
    question_7 = fields.Integer(
        string="If yes, How many do you have or plan to have?")
    question_8 = fields.Integer(string="Age of your youngest child?")

    # Step - 4
    question_11 = fields.Selection(
        select_boolean,
        string="Do you plan on paying for college?")
    question_12 = fields.Float(
        string="If Yes, by the time your child reaches college - how much do "
               "you think it will cost to send each individual child through "
               "school?")
    question_13 = fields.Selection(
        select_boolean,
        string="Do you currently have any money saved for college?")
    question_14 = fields.Float(string="If yes, what is the approx balance of "
                                      "your college savings?")
    question_14_1 = fields.Float(
        store="True", compute="_compute_college_saving",
        string="Total College Expense")
    question_14_2 = fields.Float(
        store="True", compute="_compute_college_saving",
        string="Total Remaining College Expense")

    @api.depends('question_7', 'question_12', 'question_14')
    def _compute_college_saving(self):
        if self.question_7 and self.question_12:
            self.question_14_1 = self.question_7 * self.question_12
        if self.question_14 and self.question_14_1:
            self.question_14_2 = self.question_14_1 - self.question_14
        elif self.question_14 == False and self.question_14_1:
            self.question_14_2 = self.question_14_1

    # Step - 5
    question_15 = fields.Selection(select_boolean,
                                   string="Do you have have a mortgage?")
    question_16 = fields.Float(
        string="If Yes, What is your mortgage balance?")
    question_17 = fields.Selection(
        select_boolean,
        string="Do you own money on credit cards?")
    question_18 = fields.Float(
        string="If Yes What is your credit Card Balance?")
    question_19 = fields.Selection(select_boolean,
                                   string="Do you have car payments?")
    question_20 = fields.Float(
        string="If yes what are your car payments balances?")
    question_21 = fields.Selection(
        select_boolean,
        string="Do you have any additional Debt (student loans, "
               "personal loans, etc.)")
    question_22 = fields.Float(
        string="If Yes, What is the total balance you owe?")
    question_22_1 = fields.Float(store="True", compute="_compute_total_deb",
                                 string="Total Debt")

    @api.depends('question_16', 'question_18', 'question_20', 'question_22')
    def _compute_total_deb(self):
        self.question_22_1 = sum([
            self.question_16, self.question_18,
            self.question_20, self.question_22
        ])

    # Step - 6
    question_23 = fields.Float(
        string="If you own your own home what are your annual property taxes? "
               "If you rent, what is your monthly rent?")
    question_24 = fields.Float(string="What is the cost of your Homeowners or "
                                      "renters insurance policy annually?")
    question_24_1 = fields.Float(store="True", compute="_compute_property_tax",
                                 string="Total")

    @api.depends('question_5_2', 'question_23', 'question_24')
    def _compute_property_tax(self):
        self.question_24_1 = self.question_23 + self.question_24 + self.question_5_2

    question_25 = fields.Selection(
        select_boolean,
        string="Are you responsible for paying HOA fees?")
    question_26 = fields.Float(
        string="If yes, what is your monthly HOA amount?")
    question_27 = fields.Float(
        string="Excluding your Mortgage Payment, Credit Card Payments, Car "
               "Payments, or the cost of any additional debt, how much per "
               "month do you spend on additional living expenses (Food, Fuel, "
               "Electricity, Gas, Private School, Entertainment, Landscaping, "
               "Cleaning services, etc)?")
    question_27_1 = fields.Float(store="True", compute="_compute_annual_recurring_expenses",
                                 string="Total annual Recurring expenses "
                                        "minus remaining spousal income")
    # question_27_2 = fields.Float(store="True", compute="_compute_annual_recurring_expenses",
    #                              string="Recurring expenses multiplied by the "
    #                                     "amount of years until retirement")
    question_27_3 = fields.Float(store="True", compute="_compute_annual_recurring_expenses",
                                 string="Total Benefit needed to cover recurring annual expenses minus spousal income")


    @api.depends('question_5_3', 'question_24_1',
                 'question_26', 'question_27', 'remaining_age')
    def _compute_annual_recurring_expenses(self):
        for rec in self:
            amount = rec.question_24_1 + rec.question_26 * 12 + rec.question_27 * 12 - rec.question_5_3
            rec.question_27_1 = amount
            # rec.question_27_2 = amount * rec.remaining_age
            rec.question_27_3 = amount * 0.05

    total_insurance = fields.Float(
        store="True", compute='_compute_total_calculation',
        string="Calculating how much life insurance you need")

    @api.depends('question_14_2', 'question_22_1', 'question_27_3')
    def _compute_total_calculation(self):
        self.total_insurance = sum([
            self.question_14_2,
            self.question_22_1,
            # self.question_27_2
            self.question_27_3
        ])

    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female')
    ], string="Gender")
    quote_state = fields.Char(string="State")
    smoke = fields.Boolean(string="Do You Smoke?")
    policy_type = fields.Selection([
        ('10 Year Level Term', '10 Year Level Term'),
        ('15 Year Level Term', '15 Year Level Term'),
        ('20 Year Level Term', '20 Year Level Term'),
        ('30 Year Level Term', '30 Year Level Term'),
        ('Life Coverage', 'Life Coverage'),
    ], string="Policy Type")
    rate_your_health = fields.Selection([
        ('0', 'Low'),
        ('1', 'Star : 1'),
        ('2', 'Star : 2'),
        ('3', 'Star : 3'),
        ('4', 'Star : 4'),
        ('5', 'Star : 5'),
    ], size=1, string="Rate Your Health")

    @api.constrains('question_1', 'question_2')
    def _check_age(self):
        for res in self:
            if res.question_1 > res.question_2:
                raise ValueError(_('Please add valid age.'))

    @api.depends('question_1', 'question_2')
    def _compute_age(self):
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
        if vals.get('state', '') in ['done', 'requested_quote']:
            self.sudo().send_form_mail()
        return res, self.sudo().send_form_mail_admin()

    @api.multi
    def send_form_mail(self):
        template = self.env.ref(
            'cap_web_free_quote.mail_customer_life_insurance_estimate_form',
            raise_if_not_found=False)
        template.send_mail(self.id)

    @api.multi
    def send_form_mail_admin(self):
        template = self.env.ref(
            'cap_web_free_quote.mail_customer_life_insurance_estimate_form_admin',
            raise_if_not_found=False)
        template.send_mail(self.id)

    @api.multi
    def unlink(self):
        try:
            for res in self:
                super(LifeInsuranceEstimate, res).unlink()
        except Exception as e:
            return False
        return True

    def get_quote_link(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url'
        ) + '/life/insurance-done?reference=' + self.ref_code

    def get_subject(self):
        if self.state == 'done':
            return 'Life Insurance Estimation'
        else:
            return 'Requested Quote for Life Insurance Estimation'
