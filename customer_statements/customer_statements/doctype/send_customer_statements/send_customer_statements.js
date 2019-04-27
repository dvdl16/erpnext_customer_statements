// Copyright (c) 2019, Dirk van der Laarse and contributors
// For license information, please see license.txt


frappe.ui.form.on("Send Customer Statements", "send_customer_statements", function(frm) {
	cur_frm.save();
	frappe.call({
		method: "customer_statements.api.send_statements",
		args: {
		},
		callback: function(r) {
		}
	});
});


frappe.ui.form.on("Send Customer Statements", "onload", function(frm) {
	cur_frm.save();
});

frappe.ui.form.on("Send Customer Statements", "refresh_list", function(frm) {
	cur_frm.save();
});
