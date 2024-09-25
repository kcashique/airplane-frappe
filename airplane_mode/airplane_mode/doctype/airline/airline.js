// Copyright (c) 2024, ashique and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
        if (frm.doc.website){
            frm.dashboard.add_section('<a href="' + frm.doc.website + '" target="_blank">' + __('Visit Official Website') + '</a>');
        }

	},
});
