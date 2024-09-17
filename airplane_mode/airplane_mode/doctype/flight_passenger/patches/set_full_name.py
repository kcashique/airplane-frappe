import frappe

def execute():
    passengers = frappe.db.get_all("Flight Passenger", pluck="name")
    
    for p in passengers:
        passenger = frappe.get_doc("Flight Passenger", p)
        passenger.set_full_name
        passenger.save()

    frappe.db.commit()
