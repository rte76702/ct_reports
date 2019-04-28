// Copyright (c) 2016, rte76702 and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Sales Report"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd":1,
		},
		{
			"fieldname":"start",
			"label": __("From Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.add_days(frappe.datetime.now_datetime(),-1),
			"reqd": 1
		},
		{
			"fieldname":"end",
			"label": __("To Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.now_datetime(),
		},
		{
			"fieldname":"show_customers",
			"label": __("Show Customers"),
			"fieldtype": "Check",
			"default": 0,
		},
		{
			"fieldname":"paid_only",
			"label": __("Paid Invoice Only"),
			"fieldtype": "Check",
			"default": 0,
		},
	]
}
