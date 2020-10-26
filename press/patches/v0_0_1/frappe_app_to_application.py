# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute():
	from_doctype = "Frappe App"
	to_doctype = "Application"
	if frappe.db.table_exists(from_doctype) and not frappe.db.table_exists(to_doctype):
		frappe.rename_doc("DocType", from_doctype, to_doctype, force=True)
