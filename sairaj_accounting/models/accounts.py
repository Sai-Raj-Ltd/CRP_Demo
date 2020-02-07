# -*- coding: utf-8 -*-

from odoo import models, fields, api



class AccountInvoice(models.Model):
	_inherit = "account.invoice"



	vat_registered = fields.Boolean(string = 'VAT Registered',track_visibility='onchange')
	vat_withheld  = fields.Boolean(string = 'VAT Withheld',track_visibility='onchange')
	withhold_amount = fields.Float(string = 'Withhold Amount',track_visibility='onchange')
	withhold_recieved = fields.Boolean(string = 'Withhold Recieved',track_visibility='onchange')
	certificate_no = fields.Char(string = 'Certificate No',track_visibility='onchange')
	certificate_date = fields.Date(string = 'Certificate Date',track_visibility='onchange')
	vendor_withheld = fields.Boolean(string = '2% With Held?',track_visibility='onchange')
	vendor_amount = fields.Float(string = 'Amount')
	withheld_paid = fields.Boolean(string = '2% With Held Paid?',track_visibility='onchange')
	ven_cert_date = fields.Date(string = 'Certificate Date',track_visibility='onchange')
	ven_cert_no = fields.Char(string = 'Certificate No',track_visibility='onchange')
	ven_inv_no = fields.Char(string = 'Vendor Invoice No',track_visibility='onchange')
	# remaining_inv_bal = fields.Float(string = 'Remaining Inv Balance')
	# remaining_bill_bal = fields.Float(string = 'Remaining Bill Balance')
	# intrest_per = fields.Float(string = 'Intrest(%)',track_visibility='onchange')
	# intrest_amt = fields.Float(string = 'Intrest amount',track_visibility='onchange')


	# @api.onchange('withhold_amount','amount_total','withhold_recieved')
	# def onchange_remaining_inv_bal(self):
	# 	if self.withhold_recieved == False:
	# 		if self.withhold_amount > 0.0:
	# 			self.remaining_inv_bal = self.amount_total - self.withhold_amount
	# 		else:
	# 			self.remaining_inv_bal = 0.0
	# 	else:
	# 		self.withhold_amount =0.0
	# 		self.remaining_inv_bal = 0.0


	# @api.onchange('vendor_amount','amount_total','withheld_paid')
	# def onchange_remaining_bill_bal(self):
	# 	if self.withheld_paid == False:
	# 		if self.vendor_amount > 0.0:
	# 			self.remaining_bill_bal = self.amount_total - self.vendor_amount
	# 		else:
	# 			self.remaining_bill_bal = 0.0
	# 	else:
	# 		self.vendor_amount =0.0
	# 		self.remaining_bill_bal = 0.0

	
















class accountpayments(models.Model):
	_inherit = 'account.payment'


	online_payment_method = fields.Selection([('mpesa','M-Pesa'),('visa_card','Visa Card')],string="Digital Payment Method")
	payment_refernce = fields.Char(string = "Payment Reference")
	

