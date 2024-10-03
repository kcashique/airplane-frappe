# Copyright (c) 2024, ashique and contributors
# For license information, please see license.txt

import frappe
import random
import string

from frappe.model.document import Document
from frappe import _

class AirplaneTicket(Document):

	def before_insert(self):
		# Generating Random int between 01 - 99
		random_num = random.randint(1,99)
		formatted_number = str(random_num).zfill(2)

		# Generating Random letters 
		random_letter = random.choice(['A', 'B', 'C', 'D', 'E'])

		# Setting the seat field name
		self.seat = f"{formatted_number}{random_letter}" 

		#Counting the ticket
		flight_doc = frappe.get_doc("Airplane Flight", self.flight)
		airplane_doc = frappe.get_doc("Airplane", flight_doc.airplane)

		ticket_count = frappe.db.count("Airplane Ticket", {"flight": self.flight})

		if ticket_count >= airplane_doc.capacity:
			frappe.throw(_("Cannot create a new ticket. The airplane capacity of {0} seats has been reached.").format(airplane_doc.capacity))

	
	def validate(self):
		unique_add_on = []
		item = set()

		for addon in self.add_ons:
			if addon.item not in item:
				item.add(addon.item)
				unique_add_on.append(addon)

		self.add_ons = unique_add_on

		#calculate Total amount
		total_add_on_amount = sum([addon.amount for addon in self.add_ons])
		self.total_amount = self.flight_price + total_add_on_amount
	
	# def before_submit(self):
	# 	# Prevent submission if status is not 'Boarded'
	# 	if self.status != "Boarded":
	# 		# Raise error to prevent submission
	# 		frappe.throw(_("You cannot submit this ticket unless the status is 'Boarded'"))
