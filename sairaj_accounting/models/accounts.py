# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
# import pdb




class AccountInvoice(models.Model):
	_inherit = "account.invoice"



	vat_registered = fields.Boolean(string = 'VAT Registered',track_visibility='onchange')
	vat_withheld  = fields.Boolean(string = 'VAT Withheld',track_visibility='onchange')
	withhold_amount = fields.Float(string = 'WH VAT Amount',track_visibility='onchange')
	withheld_per = fields.Float(string = 'Withheld Percentage')
	withheld_amt_tree = fields.Float(string = 'Withheld Amount')
	withhold_recieved = fields.Boolean(string = 'WH VAT certificate received',track_visibility='onchange')
	certificate_no = fields.Char(string = 'Certificate No',track_visibility='onchange')
	certificate_date = fields.Date(string = 'Certificate Date',track_visibility='onchange')
	vendor_withheld = fields.Boolean(string = 'Withheld?',track_visibility='onchange')
	vendor_amount = fields.Float(string = 'Withheld Amount')
	ven_amt_tree = fields.Float(string = '')
	withheld_paid = fields.Boolean(string = 'Withheld Amount Paid?',track_visibility='onchange')
	ven_cert_date = fields.Date(string = 'Certificate Date',track_visibility='onchange')
	ven_cert_no = fields.Char(string = 'Certificate No',track_visibility='onchange')
	ven_inv_no = fields.Char(string = 'Vendor Invoice No',track_visibility='onchange')
	remaining_inv_bal = fields.Float(track_visibility='onchange',compute = '_compute_remaining_inv_bal',store= True)
	remaining_bill_bal = fields.Float(track_visibility='onchange',compute = '_compute_remaining_bill_bal',store = True)
	ven_withheld_per = fields.Float(string ='Withheld Percentage',track_visibility='onchange')
	ven_vat_registered = fields.Boolean(string = "VAT Registered")
	# intrest_per = fields.Float(string = 'Intrest(%)',track_visibility='onchange')
	# intrest_amt = fields.Float(string = 'Intrest amount',track_visibility='onchange')


#---------------------Remaining Invoice balance calculation---------------------------------------------------------

	@api.depends('withheld_amt_tree','amount_total','withhold_recieved','residual')
	def _compute_remaining_inv_bal(self):
		for record in self:

			if record.withhold_recieved == False and record.residual == 0.0:
				record.remaining_inv_bal = 0.0
			elif record.withhold_recieved == False and record.residual > 0.0:
				if record.withheld_amt_tree >= 0.0:
					record.remaining_inv_bal = record.residual - record.withheld_amt_tree
				else:
					record.remaining_inv_bal = 0.0
			elif record.withhold_recieved == True and record.residual == 0.0:
				record.remaining_inv_bal = 0.0
			elif record.withhold_recieved == True and record.residual > 0.0:
				if record.withheld_amt_tree == 0.0:
					record.remaining_inv_bal = record.residual - record.withheld_amt_tree
			# elif record.withhold_recieved == True and record.residual > 0.0:
			# 	if record.withhold_amount > 0.0:
			# 		record.remaining_inv_bal = record.residual - record.withhold_amount
			# 	else:
			# 		record.remaining_inv_bal = 0.0


			

#------------------------Remaining Bill Balance Calculation------------------------------------------------------------

	@api.depends('ven_amt_tree','amount_total','withheld_paid','residual')
	def _compute_remaining_bill_bal(self):
		for record in self:

			if record.withheld_paid == False and record.residual == 0.0:
				record.remaining_bill_bal = 0.0
				
			elif record.withheld_paid == False and record.residual > 0.0:
				if record.ven_amt_tree >= 0.0:
					record.remaining_bill_bal = record.residual - record.ven_amt_tree
				else:
					record.remaining_bill_bal = 0.0
			elif record.withheld_paid == True and record.residual > 0.0:
				if record.ven_amt_tree == 0.0:
					record.remaining_bill_bal = record.residual - record.ven_amt_tree
			elif record.withheld_paid == True and record.residual == 0.0:
				record.remaining_bill_bal =0.0


		



#---------------------Invoice Withheld amount calculations--------------------------------------------------------------



	@api.onchange('vat_withheld','withheld_per','amount_untaxed','withhold_recieved')
	def onchange_withheld_amt(self):
		
		if self.vat_withheld == True and self.withhold_recieved == False:
			if self.withheld_per>0.0:
				self.withhold_amount = (self.withheld_per)/100 * self.amount_untaxed
				self.withheld_amt_tree = (self.withheld_per)/100 * self.amount_untaxed
			else:
				self.withhold_amount = 0.0
				# self.withheld_amt_tree =0.0
		else:
			# self.withheld_per =0.0
			self.withheld_amt_tree = 0.0



#----------------------Vendor Witheld amount calculation---------------------------------------------------------------


	@api.onchange('vendor_withheld','ven_withheld_per','amount_untaxed','withheld_paid')
	def onchange_vendor_withheld_amt(self):
		if self.vendor_withheld == True and self.withheld_paid== False:
			if self.ven_withheld_per>0.0:
				self.vendor_amount = (self.ven_withheld_per)/100 * self.amount_untaxed
				self.ven_amt_tree =  (self.ven_withheld_per)/100 * self.amount_untaxed
			else:
				self.vendor_amount = 0.0
				# self.ven_amt_tree = 0.0
		else:
			# self.ven_withheld_per =0.0
			self.ven_amt_tree = 0.0







class AccountAssetCategory(models.Model):

	_inherit = 'account.asset.category'

	method_progress_factor = fields.Float('Degressive Factor', default=0.3,digits=(12,3))



class AccountAssetAsset(models.Model):
	_inherit = 'account.asset.asset'


	method_progress_factor = fields.Float(string='Degressive Factor', readonly=True, default=0.3, digits=(12,3),states={'draft': [('readonly', False)]})



	
















class accountpayments(models.Model):
	_inherit = 'account.payment'


	online_payment_method = fields.Selection([('mpesa','M-Pesa'),('visa_card','Visa Card')],string="Digital Payment Method")
	payment_refernce = fields.Char(string = "Payment Reference")





	

