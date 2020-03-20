# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

from odoo import models, fields, api


class OnlineInsuranceApplication(models.Model):
    _name = 'online.insurance.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Online Insurance Application'

    select_boolean = [('Yes', 'Yes'), ('No', 'No')]

    name = fields.Char(string="Log")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done')
    ], string="Status", default="draft", track_visibility="onchange")

    # Step - 1
    question_1 = fields.Char(string="First Name")
    question_2 = fields.Char(string="Last Name")
    question_3 = fields.Date(string="Date of Birth")
    question_4 = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
    ], string="Sex")
    question_5 = fields.Char(string="Home Street Address")
    question_6 = fields.Char(string="Home City")
    question_7 = fields.Char(string="Home State")
    question_8 = fields.Char(string="Home Zip")
    question_9 = fields.Char(string="Phone Number",
                             track_visibility="onchange")
    question_10 = fields.Char(string="Email Address",
                              track_visibility="onchange")

    # Step - 2
    question_11 = fields.Char(string="Social Security Number")
    question_12 = fields.Char(string="Drivers License Number")
    question_13 = fields.Char(string="License Issue State")
    question_14 = fields.Date(string="License Expiration Date")
    question_15 = fields.Char(string="Years lived at the current address?")
    question_16 = fields.Char(string="Country/State of birth")
    question_17 = fields.Selection(select_boolean, default="No",
                                   string="Are you a US Citizen?")
    question_18 = fields.Char(string="If no, Visa type")
    question_19 = fields.Char(string="Visa Number")
    question_20 = fields.Char(string="Number of years residing in the US")
    question_21 = fields.Char(string="Employer Name")
    question_22 = fields.Char(string="Employer Street Address")
    question_23 = fields.Char(string="Employer City")
    question_24 = fields.Char(string="Employer State")
    question_25 = fields.Char(string="Employer Zip Code")
    question_26 = fields.Char(string="Occupation/Specialty")
    question_27 = fields.Char(string="Occupational duties")

    # Step - 3
    question_28 = fields.Integer(
        string="The total number of years working in this occupation?")
    question_29 = fields.Integer(
        string="The total number of years with the same employer?")
    question_30 = fields.Selection(select_boolean, default="No",
                                   string="Do you work at least 30 "
                                          "hours per week?")
    question_31 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever had a professional license suspended or revoked,"
               " or is such license currently under review?")
    question_32 = fields.Char(string="If yes, please explain?")
    question_33 = fields.Selection(
        select_boolean, default="No",
        string="Do you have any ownership in the business where you work?")
    question_34 = fields.Float(string="If yes, what percentage do you own?")
    question_35 = fields.Selection([
        ('LLC', 'LLC'),
        ('S-Corp', 'S-Corp'),
        ('Other', 'Other'),
    ], string="If Yes, what type of business is it?")
    question_36 = fields.Selection(
        select_boolean, default="No",
        string="Are there more than 10 people employed "
               "with your current employer?")
    question_37 = fields.Char(
        string="What is your current projected YTD income?")
    question_38 = fields.Float(
        string="What was last year's Adjusted Gross Income Total?")
    question_39 = fields.Float(
        string="What was 2 years ago Adjusted Gross Income Total?")
    question_40 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever filed for personal or business bankruptcy?")
    question_41 = fields.Char(
        string="If Yes, please provide details including discharge date")

    # Step - 4
    question_42 = fields.Selection(
        select_boolean, default="No",
        string="Do you have any existing Group or "
               "Individual Disability Insurance?")
    question_43 = fields.Char(string="If Yes, Carrier 1 name?")
    question_44 = fields.Char(string="Carrier 2 name?")
    question_45 = fields.Char(
        string="Carrier 1 total monthly benefit amount?")
    question_46 = fields.Char(
        string="Carrier 2 total monthly benefit amount?")
    question_47 = fields.Selection(select_boolean, default="No",
                                   string="Is Carrier 1 employer paid?")
    question_48 = fields.Selection(select_boolean, default="No",
                                   string="Is Carrier 2 employer paid?")
    question_49 = fields.Selection(
        select_boolean, default="No",
        string="Will you be replacing any of your existing coverage?")
    question_50 = fields.Char(
        string="Do you want to provide any additional details "
               "regarding your current coverage?")
    question_51 = fields.Selection(
        select_boolean, default="No",
        string="Have you used tobacco or nicotine products in "
               "any form within the last 5 years?")
    question_52 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever applied for insurance or reinstatement "
               "which has been: Declined, Postponed, Rated, or Modified?")
    question_53 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever received or claimed disability benefits "
               "for any injury, sickness or impaired condition?")
    question_54 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever made any flights as a pilot,"
               " student pilot, or crew member of any aircraft?")
    question_55 = fields.Selection(
        select_boolean, default="No",
        string="Have you been convicted of a moving violation,"
               " had any traffic accidents, or had a driver's license "
               "revoked or suspended within the past 5 years?")
    question_56 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been charged with, or convicted of, or currently"
               " awaiting trial on the violation of any criminal law?")
    question_57 = fields.Selection(
        select_boolean, default="No",
        string="Do you belong to or intend to join "
               "the military in the next two years?")
    question_58 = fields.Selection(
        select_boolean, default="No",
        string="Engaged in or plan to engage in the next two years in any form"
               " of the following: Motorized Racing, Parachuting/Skydiving, "
               "Martial Arts, Scuba Diving, Mountain Climbing?")
    # question_59 = fields.Char(
    #     string="Provide details to any of the 8 questions "
    #            "above where you answered: Yes")
    question_51_details = fields.Char(
        string="If yes, please provide details")
    question_52_details = fields.Char(
        string="If yes, please provide details")
    question_53_details = fields.Char(
        string="If yes, please provide details")
    question_54_details = fields.Char(
        string="If yes, please provide details")
    question_55_details = fields.Char(
        string="If yes, please provide details")
    question_56_details = fields.Char(
        string="If yes, please provide details")
    question_57_details = fields.Char(
        string="If yes, please provide details")
    question_58_details = fields.Char(
        string="If yes, please provide details")
    # Step - 5
    question_60 = fields.Char(string="What is your Height?")
    question_61 = fields.Char(string="What is your weight?")
    question_62 = fields.Selection(
        select_boolean, default="No",
        string="Have you seen a doctor within the past 5 years?")
    question_63 = fields.Char(
        string="If Yes, Please list all your doctor's names - Addresses - Telephone Numbers - Date of your last visit - Reason for your last visit.")
    question_64 = fields.Selection(
        select_boolean, default="No",
        string="Do you currently take any prescription medications?")
    question_65 = fields.Char(
        string="If Yes, please list all medications names - doses - and the reason you are taking the medication.")
    question_66 = fields.Selection(
        select_boolean, default="No",
        string="Has your weight changed by more than 10 lbs in the last twelve months?")
    question_67 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed with High Blood Pressure or High Cholesterol?")
    question_68 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed with dizziness, vertigo, fainting, seizures, recurrent headache, speech defect, tremor, neuropathy, paralysis, multiple sclerosis, stroke, TIA, memory loss, dementia or any other disorder of the brain or nervous system?")
    question_69 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having shortness of breath, chronic cough, bronchitis, asthma, emphysema, COPD, sleep apnea, or chronic respiratory disorder?")
    question_70 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having chest pain, irregular heartbeat, heart murmur, heart valve disease, heart attack, coronary artery disease, heart failure, aneurysm or other heart or blood vessel disorder?")
    question_71 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having intestinal "
               "bleeding, inflammatory bowel disease (including Crohn's "
               "disease or ulcerative colitis), hepatitis, diverticulitis, "
               "recurrent indigestion or any other esophagus, stomach, "
               "intestines, pancreas, liver or gallbladder disorder?")
    question_72 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having sugar, "
               "protein, or blood in the urine; sexually transmitted disease"
               " (excluding HIV) chronic kidney disease, kidney stone "
               "or other kidney or bladder issues?")
    question_73 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having diabetes, "
               "elevated blood sugar, thyroid, pituitary, "
               "adrenal or any other endocrine (glandular) disorders?")
    question_74 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having breast,"
               " reproductive organ or prostate disorder?")
    question_75 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever had a C-section, miscarriage, "
               "or complication of pregnancy?")
    question_76 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as "
               "having a mass, polyp, cyst, tumor or cancer?")
    question_77 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having allergies, "
               "skin disorders, anemia, bleeding, clotting, "
               "or other blood disorder?")
    question_78 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having anxiety,"
               " depression, stress, ADHD, eating disorder or other "
               "psychiatric or mental health disorders?")
    question_79 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever been treated or diagnosed as having "
               "chronic fatigue, chronic pain, fibromyalgia, "
               "or fever of unknown cause?")
    question_80 = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('N/A', 'N/A'),
    ], default="N/A", string="Are you currently pregnant?")
    question_81 = fields.Selection(
        select_boolean, default="No",
        string="In the last 5 years have you received "
               "treatment from a licensed Chiropractor?")
    question_82 = fields.Selection(
        select_boolean, default="No",
        string="In the last 5 years have you sought treatment from a licensed"
               " medical professional, had a checkup, illness, injury, or "
               "surgery; been a patient in a hospital; rehabilitation center "
               "or another medical facility; had an X-ray, EKG, heart scan, "
               "MRI or CT scan, biopsy or another diagnostic testing?")
    question_83 = fields.Selection(
        select_boolean, default="No",
        string="In the last 5 years have you been advised by a licensed "
               "medical professional to have any diagnostic testing, "
               "hospitalization, or surgery which has not been completed?")
    question_84 = fields.Selection(
        select_boolean, default="No",
        string="In the last 10 years have you used marijuana, cocaine, heroin,"
               " barbiturates, tranquilizers, hallucinogens, amphetamines, "
               "narcotics, or any other drug, except as legally "
               "prescribed by a physician?")
    question_85 = fields.Selection(
        select_boolean, default="No",
        string="In the last 10 years have you sought, received or been "
               "advised to seek medical treatment from a licensed medical "
               "profession, counseling or participation in a support group "
               "for the use of alcohol or illegal drugs?")

    question_83_details = fields.Char(
        string="If yes, please provide details")
    question_84_details = fields.Char(
        string="If yes, please provide details")
    question_85_details = fields.Char(
        string="If yes, please provide details")

    # question_86 = fields.Char(
    #     string="Please provide details to any of the above "
    #            "questions where you answered : yes")
    question_87 = fields.Selection(
        select_boolean, default="No",
        string="In the past 10 years have you consumed alcoholic beverages?")
    question_88 = fields.Char(string="If yes, how often do you drink?")
    question_89 = fields.Selection(
        select_boolean, default="No",
        string="Have you ever tested positive for HIV or Aids?")
    question_89_details = fields.Char(
        string="If yes, please provide details")
    question_90 = fields.Selection(
        select_boolean, default="No",
        string="To the best of your knowledge, have any of your immediate "
               "family members (Mother - Father - Sister - Brother) died of or"
               " been diagnosed as having coronary artery disease, stroke, "
               "diabetes, cancer, polycystic kidney disease, or Huntington's "
               "disease prior to their age of 60?")
    question_91 = fields.Char(
        string="Please provide details if you answered yes")
    question_92 = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Unknown', 'Unknown'),
    ], default="Unknown", string="Is your father still living?")
    question_93 = fields.Char(
        string="If Yes, how old is he - If No, At what age did he die and what was his cause of death?")
    question_94 = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Unknown', 'Unknown'),
    ], default="Unknown", string="Is your mother still living?")
    question_95 = fields.Char(
        string="If Yes, how old is she - If No, At what age did she die and what was her cause of death?")
    question_96 = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('N/A', 'N/A'),
    ], default="N/A", string="Are all your siblings still living?")
    question_97 = fields.Char(
        string="If Yes How old is each one - If No, at what age did "
               "they die and what was their cause of death?")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'online.insurance.application')
        return super(OnlineInsuranceApplication, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(OnlineInsuranceApplication, self).write(vals)
        if vals.get('state', '') == 'done':
            self.send_form_mail()
        return res

    @api.multi
    def send_form_mail(self):
        # template = self.env.ref(
        #     'cap_web_free_quote.mail_life_insurance_estimate_form',
        #     raise_if_not_found=False)
        # template.send_mail(self.id)
        template = self.env.ref(
            'cap_web_free_quote.mail_customer_online_insurance_application_form',
            raise_if_not_found=False)
        template.send_mail(self.id)
