# Copyright (c) 2013, rte76702 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime, time, date
from frappe.utils import get_datetime
from frappe.desk.reportview import get_filters_cond
from frappe.utils import get_link_to_form


def execute(filters=None):
	filters = filters or {}
	columns, data = [], []

	columns = [
		'Item Group:Link/Item Group:120',
		'Item:Link/Item:120',
		'Customer:Link/Customer:120',
		'Total Qty:Int:50',
		'Total Amt:Currency:100',
		'Invoices:Data:150'
	]

	start = get_datetime(filters.get('start'))
	end = get_datetime(filters.get('end'))
	paid_only = filters.get('paid_only')
	company = filters.get('company')
	show_cust = filters.get('show_customers')
	group_by = '`tabSales Invoice Item`.item_code'

	filters = {'company': company}
	if paid_only:
		filters['outstanding_amount'] = 0
	if show_cust:
		group_by += ', `tabSales Invoice`.customer'

	query = '''SELECT * FROM (SELECT 
		GROUP_CONCAT(`tabSales Invoice`.name SEPARATOR ',') as names,
		`tabSales Invoice Item`.item_code,
		`tabSales Invoice Item`.item_group,
		SUM(`tabSales Invoice Item`.qty) as qty,
		SUM(`tabSales Invoice Item`.amount) as amount,
		`tabSales Invoice`.customer,`tabSales Invoice`.posting_time,
		`tabSales Invoice`.posting_date,
		ADDTIME(`tabSales Invoice`.posting_date,
			`tabSales Invoice`.posting_time) as addtime
		FROM `tabSales Invoice`, `tabSales Invoice Item`
		WHERE `tabSales Invoice Item`.parent = `tabSales Invoice`.name
		AND ADDTIME(`tabSales Invoice`.posting_date,
			`tabSales Invoice`.posting_time) >= "{start}" {cond}
		GROUP BY {group_by}) as result
		ORDER BY result.item_code,
			result.posting_date desc,
			result.posting_time desc
		'''.format(cond=get_filters_cond('Sales Invoice',filters,[]),
				   group_by=group_by,
				   start=start)
	res = frappe.db.sql(query, as_dict=1)

	for r in res:
		if r.addtime > end:
			continue
		
		tmp = [
			r.item_group,r.item_code,
			r.customer,r.qty,r.amount,
		]
		if r.names.strip():
			names = [get_link_to_form('Sales Invoice',i) for i in r.names.split(',')]
			tmp.append(', '.join(names))
		if not show_cust:
			del tmp[2]
		data.append(tmp)
	
	if not show_cust:
		del columns[2]
	
	return columns, data
