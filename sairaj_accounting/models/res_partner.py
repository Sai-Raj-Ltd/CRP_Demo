

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import pdb


class ResPartnerex(models.Model):
	_inherit = 'res.partner'


	is_withholiding_agent = fields.Boolean(string = 'Is Withholding Agent',track_visibility='onchange')
	vat = fields.Char(string='KRA PIN NO', help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")
	_sql_constraints = [
				('kra_pin_unique', 'UNIQUE(vat)',
					'This KRA Pin Should be always Unique, Duplicate KRA Pin are not allowed!'),
		]

	


	@api.one
	@api.constrains('vat')
	def vat_validations(self):

		if self.vat:
			rec = list(self.vat)
			if len(rec) >= 12:
				raise ValidationError('Invalid KRA PIN, Please enter a Valid KRA PIN')
			elif len(rec) <11:
				raise ValidationError('Invalid KRA PIN, Please enter a Valid KRA PIN')
			elif not rec[0].isalpha():
				raise ValidationError('Invalid KRA PIN, Please enter a Valid KRA PIN')
			elif not rec[-1].isalpha():
				raise ValidationError('Invalid KRA PIN, Please enter a Valid KRA PIN')
			else:
				for i in range(1, 10):
					if not rec[i].isdigit():
						raise ValidationError('Invalid KRA PIN, Please enter a Valid KRA PIN')









			

