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

