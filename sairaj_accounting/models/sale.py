

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import pdb


class SaleOrder(models.Model):
	_inherit = "sale.order"

	sale_on_credit = fields.Boolean(string = 'Sale On Credit')






	@api.multi
	def check_limit(self):
		self.ensure_one()
		partner = self.env['res.partner'].search([('id','=',self.partner_id.id)])
		if self.sale_on_credit == partner.on_credit:
			limit = partner.credit_limit
			due_amt = partner.total_due
			if limit > 0.0:
				amt = limit + due_amt
				if amt >= self.amount_total:
					raise ValidationError('Customer reached a over credit limit')



	@api.constrains('amount_total','sale_on_credit')
	def check_amount(self):
		for order in self:
			order.check_limit()


	@api.multi
	def action_confirm(self):
		res = super(SaleOrder, self).action_confirm()
		for order in self:
			order.check_limit()
		return res














			

