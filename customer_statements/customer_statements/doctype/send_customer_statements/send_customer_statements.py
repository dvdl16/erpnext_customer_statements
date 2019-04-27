# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk van der Laarse and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SendCustomerStatements(Document):
	def validate(self):
		# Get list of customers and email addresses, append to table
		self.customers = [];
		customer_list = frappe.db.sql("""SELECT tab_cus.name, tab_con.email_id,
										CASE WHEN ISNULL(tab_con.email_id) OR tab_cus.disable_sending_of_customer_statements = 1 THEN 'No' ELSE 'Yes' END AS 'send_statement'
										FROM `tabCustomer` AS tab_cus
										LEFT JOIN `tabDynamic Link` as tab_dyn ON tab_dyn.link_name = tab_cus.name AND tab_dyn.link_doctype = 'Customer'
										LEFT JOIN `tabContact` as tab_con ON tab_dyn.parent = tab_con.name AND tab_dyn.parenttype = 'Contact'""", as_dict=True)
		for i in customer_list:
			row = self.append('customers', {})
			row.customer_name = i.name
			row.email = i.email_id
			row.send_statement = i.send_statement

	# def validate(self):
		# if self.get('__islocal'):
		# 	frappe.msgprint('islocal = true')
		# else:
		# 	frappe.msgprint('islocal = false')
