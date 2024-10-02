// Copyright (c) 2024, ashique and contributors
// For license information, please see license.txt
frappe.ui.form.on('Airline', {
    refresh(frm) {
        // Check if the Website field is not empty
        if (frm.doc.website) {
            // Add the web link to the form header
            frm.add_web_link(__('Official Website'), frm.doc.website);

            // Add the web link to the dashboard section
            frm.dashboard.add_section('<a href="' + frm.doc.website + '" target="_blank">' + __('Visit Official Website') + '</a>');
        }
    }
});


