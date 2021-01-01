import frappe
from frappe import _

@frappe.whitelist()
def export_on_submit(self, method):
	export_lic(self, method)
	total_export(self,method)

@frappe.whitelist()
def export_on_cancel(self, method):
	export_lic_cancel(self, method)
	total_export(self,method)
	
@frappe.whitelist()
def import_on_submit(self, method):
	import_lic(self, method)
	total_import(self,method)

@frappe.whitelist()
def import_on_cancel(self, method):
	import_lic_cancel(self, method)
	total_import(self,method)

#On Submit Export
def export_lic(self, method):
	if self.license:	
		existing_row_id = frappe.db.get_value("Export Against AAL", filters={"parent": self.license, "sales_invoice": self.name}, fieldname="name")
		
		if existing_row_id:
			existing_row = frappe.get_doc("Export Against AAL", {"parent": self.license, "sales_invoice": self.name})
			existing_row.shipping_bill_no = self.shipping_bill
			existing_row.sb_date = self.shipping_bill_date
			existing_row.quantity = self.total_qty
			existing_row.port_of_loading = self.port_of_loading
			existing_row.port_of_discharge = self.port_of_discharge
			existing_row.fob_value = self.fob_inr
			existing_row.cif_value = self.base_grand_total
			existing_row.currency = self.currency
			existing_row.save()
			frappe.db.commit()
		else:
			target_doc = frappe.get_doc("Advance Authorisation License", self.license)
			target_doc.append("exports", {
				"shipping_bill_no": self.shipping_bill,
				"sb_date": self.shipping_bill_date,
				"quantity": self.total_qty,
				"port_of_loading" : self.port_of_loading,
				"port_of_discharge" : self.port_of_discharge,
				"fob_value" : self.fob_inr,
				"cif_value" : self.base_grand_total,
				"currency" : self.currency,
				"sales_invoice" : self.name
			})
			target_doc.save()
			frappe.db.commit()

#CANCEL Export
def export_lic_cancel(self, method):
	if self.license:
		existing_row_id = frappe.db.get_value("Export Against AAL", filters={"parent": self.license, "sales_invoice": self.name}, fieldname="name")
		frappe.delete_doc("Export Against AAL", existing_row_id)
		frappe.db.commit()

#Calculate Total Export
def total_export(self,method):
	if self.license:
		target_doc = frappe.get_doc("Advance Authorisation License", self.license)
		totalexpqty = 0
		totalexpamt = 0
		for row in target_doc.exports:
				totalexpqty += row.quantity
				totalexpamt += row.fob_value
		target_doc.total_export_qty = totalexpqty
		target_doc.total_export_amount = totalexpamt
		target_doc.remaining_export_qty = target_doc.approved_qty - totalexpqty
		target_doc.remaining_export_amount = target_doc.approved_amount - totalexpamt
		target_doc.save()
		frappe.db.commit()

	
#On Submit Import
def import_lic(self, method):
	if self.license:
		existing_row_id = frappe.db.get_value("Import Against AAL", filters={"parent": self.license, "purchase_invoice": self.name}, fieldname="name")
		
		if existing_row_id:
			existing_row = frappe.get_doc("Import Against AAL", {"parent": self.license, "purchase_invoice": self.name})
			existing_row.shipping_bill_no = self.shipping_bill
			existing_row.sb_date = self.shipping_bill_date
			existing_row.quantity = self.total_qty
			existing_row.port_of_loading = self.port_of_loading
			existing_row.port_of_discharge = self.port_of_discharge
			existing_row.fob_value = self.fob_inr
			existing_row.cif_value = self.base_grand_total
			existing_row.currency = self.currency
			existing_row.save()
			frappe.db.commit()
		else:
			target_doc = frappe.get_doc("Advance Authorisation License", self.license)
			target_doc.append("imports", {
				"shipping_bill_no": self.shipping_bill,
				"sb_date": self.shipping_bill_date,
				"quantity": self.total_qty,
				"port_of_loading" : self.port_of_loading,
				"port_of_discharge" : self.port_of_discharge,
				"fob_value" : self.fob_inr,
				"cif_value" : self.base_grand_total,
				"currency" : self.currency,
				"purchase_invoice" : self.name
			})
			target_doc.save()
			frappe.db.commit()

#CANCEL Import
def import_lic_cancel(self, method):
	if self.license:
		existing_row_id = frappe.db.get_value("Import Against AAL", filters={"parent": self.license, "purchase_invoice": self.name}, fieldname="name")
		frappe.delete_doc("Import Against AAL", existing_row_id)
		frappe.db.commit()
	
def total_import(self,method):
	if self.license:
		target_doc = frappe.get_doc("Advance Authorisation License", self.license)
		totalimpqty = 0
		totalimpamt = 0
		for row in target_doc.imports:
				totalimpqty += row.quantity
				totalimpamt += row.cif_value
		target_doc.total_import_qty = totalimpqty
		target_doc.total_import_amount = totalimpamt
		target_doc.remaining_import_qty = target_doc.approved_qty - totalimpqty
		target_doc.remaining_import_amount = target_doc.approved_amount - totalimpamt
		target_doc.save()
		frappe.db.commit()