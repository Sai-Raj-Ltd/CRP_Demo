# -*- coding: utf-8 -*-

import time
import math
import re

from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


class ReleiverSigning(models.Model):
    _inherit = "hr.leave"
    _description = "Reliever Name"

    releiver_name = fields.Many2one("res.users",string='Releiver Name')


class OtherAmount(models.Model):
    _inherit = 'hr.payslip.input'
    _description = "Payslip Input Hours"

    number_of_hours = fields.Float(string='Number of Hours')
    total_amount = fields.Float(string='Total Amount', compute='_compute_amount', )

    @api.multi
    def _compute_amount(self):
        for rec in self:
            if rec.number_of_hours and rec.amount:
                for get in self:
                    get.total_amount = get.amount * get.number_of_hours

