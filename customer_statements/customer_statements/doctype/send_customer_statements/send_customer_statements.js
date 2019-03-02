// Copyright (c) 2019, Dirk van der Laarse and contributors
// For license information, please see license.txt

frappe.ui.form.on('Send Customer Statements', {
	refresh: function(frm) {

	}
});


frappe.ui.form.on("Send Customer Statements", "send_customer_statements", function(frm) {
	frappe.call({
		method: "customer_statements.api.send_statements",
		args: {
		},
		callback: function(r) {

		}
	});
});
