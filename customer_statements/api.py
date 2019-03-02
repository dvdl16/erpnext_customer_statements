from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, time_diff_in_hours, get_datetime, getdate, today, cint, add_days
from frappe import _
from frappe.utils.xlsxutils import make_xlsx


@frappe.whitelist()
def send_statements(customer):
	email_list = ['dirk@simplygarlic.co.za']
	custom_filter = {'company': "Horizon Global SA (Pty) Ltd", 'party_type': "Customer", 'party': "Freshmark", 'from_date': add_days(today(), -7),'to_date': today()}
	report = frappe.get_doc('Report', "General Ledger")
	columns, data = report.get_data(limit=100 or 100, user = "Administrator", filters = custom_filter, as_dict=True)
	columns.insert(0, frappe._dict(fieldname='idx', label='', width='30px'))
	k = 0
	for k in range(len(data)):
		data[k]['idx'] = k+1
	html = frappe.render_template('frappe/templates/includes/print_table.html', {'columns': columns,'data':data})
	#frappe.msgprint(html)
	#single_email_id = i
	#self.send_emails(html,single_email_id)

	message = '<p>{0}</p>'.format(_('{0} generated on {1}')\
			.format("subject",
				frappe.utils.format_datetime(frappe.utils.now_datetime())))

	message += '<hr style="margin: 15px 0px;">' + "self.description"
	message += '<hr>' + html
	#frappe.msgprint(single_email_id)
	#frappe.msgprint(message)
	# report_doctype = frappe.db.get_value('Report', self.report, 'ref_doctype')
	# report_footer = frappe.render_template(self.get_report_footer(),dict(report_url = frappe.utils.get_url_to_report("DPI Task Report", "Script Report", "Task"),report_name = "DPI Task Report"))
	#rec = self.cc.split(",")
	#rec.insert(0,single_email_id)
	#rec = ",".join(rec)
	frappe.sendmail(
		recipients = 'dirktemp16@gmail.com',
		subject = 'self.subject',
		message = message,
		attachments = None
	)
	frappe.msgprint('Email sent')


@frappe.whitelist()
def send_statements2(customer):

	data = get_report_content()
	if not data:
		return

	#attachments = None
	#if self.format == "HTML":
#		message = data
#	else:
#		message = self.get_html_table()


	attachments = [{
		'fname': get_file_name(),
		'fcontent': data
	}]

	frappe.sendmail(
		recipients = 'dirktemp16@gmail.com',
		subject = "Report",
		message = "message",
		attachments = attachments,
		reference_doctype = "Report",
		reference_name="General Ledger"
	)

	frappe.msgprint('Email sent with method 2')

def get_report_content():
	'''Returns file in for the report in given format'''

	report = frappe.get_doc('Report', "General Ledger")
	custom_filter = {'company': "Horizon Global SA (Pty) Ltd", 'party_type': "Customer", 'party': "Freshmark", 'from_date': add_days(today(), -7),'to_date': today(), 'group_by': "Group by Voucher (Consolidated)"}

	columns, data = report.get_data(limit=100 or 100, user = "Administrator", filters = custom_filter, as_dict=True)

	# add serial numbers
	columns.insert(0, frappe._dict(fieldname='idx', label='', width='30px'))
	for i in range(len(data)):
		data[i]['idx'] = i+1


	spreadsheet_data = get_spreadsheet_data(columns, data)
	xlsx_file = make_xlsx(spreadsheet_data, "Auto Email Report")
	return xlsx_file.getvalue()


def get_spreadsheet_data(columns, data):
	out = [[_(df.label) for df in columns], ]
	for row in data:
		new_row = []
		out.append(new_row)
		for df in columns:
			if df.fieldname not in row: continue
			new_row.append(frappe.format(row[df.fieldname], df, row))

	return out

def get_file_name():
	return "{0}.{1}".format("General Ledger".replace(" ", "-").replace("/", "-"), "xlsx")
