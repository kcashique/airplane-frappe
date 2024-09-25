// Copyright (c) 2024, ashique and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        frm.add_custom_button(__('Assign Seat'), function() {
            // Show a dialog to input seat number
            let d = new frappe.ui.Dialog({
                title: __('Assign Seat Number'),
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Assign',
                primary_action(values) {
                    // Set the seat field in the form
                    frm.set_value('seat', values.seat_number);
                    d.hide();
                }
            });
            
            // Show the dialog
            d.show();
        }, __("Actions"));
    }
});
