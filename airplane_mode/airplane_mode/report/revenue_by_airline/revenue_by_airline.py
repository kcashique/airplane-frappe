# # Copyright (c) 2024, ashique and contributors
# # For license information, please see license.txt

import frappe
from frappe import _


# def execute(filters: dict | None = None):
# 	"""Return columns and data for the report.

# 	This is the main entry point for the report. It accepts the filters as a
# 	dictionary and should return columns and data. It is called by the framework
# 	every time the report is refreshed or a filter is updated.
# 	"""
# 	# columns = get_columns()
# 	# data = get_data()

# 	# return columns, data




# def get_columns() -> list[dict]:
# 	"""Return columns for the report.

# 	One field definition per column, just like a DocType field definition.
# 	"""
# 	return [
# 		{
# 			"label": _("Column 1"),
# 			"fieldname": "column_1",
# 			"fieldtype": "Data",
# 		},
# 		{
# 			"label": _("Column 2"),
# 			"fieldname": "column_2",
# 			"fieldtype": "Int",
# 		},
# 	]


# def get_data() -> list[list]:
# 	"""Return data for the report.

# 	The report data is a list of rows, with each row being a list of cell values.
# 	"""
# 	return [
# 		["Row 1", 1],
# 		["Row 2", 2],
# 	]

def execute(filters=None):
    columns, data = [], []

    # Define columns for the report
    columns = [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150
        }
    ]
    
    # SQL Query to fetch revenue by airlines (including airlines with 0 revenue)
    data = frappe.db.sql("""
        SELECT
			a.name AS airline,  -- Fetch the airline name
			COALESCE(SUM(at.total_amount), 0) AS revenue  -- Sum the total amount for each ticket, defaulting to 0 if NULL
		FROM
			`tabAirline` a  -- Start with the airline table
		LEFT JOIN
			`tabAirplane` b ON a.name = b.airline  -- Join with the airplane table
		LEFT JOIN
			`tabAirplane Flight` f ON b.name = f.airplane  -- Join with the flight table
		LEFT JOIN
			`tabAirplane Ticket` at ON f.name = at.flight  -- Join with the ticket table
		GROUP BY
			a.name  -- Group by airline name
		ORDER BY
			revenue DESC;  -- Sort airlines by revenue (highest to lowest)
    """, as_dict=True)

    # Calculate the total revenue
    total_revenue = sum([row["revenue"] for row in data])

    # Append total row at the end
    data.append({
        "airline": "Total",
        "revenue": total_revenue
    })

    # Donut Chart Data
    chart = {
        "data": {
            "labels": [row["airline"] for row in data[:-1]],  # Exclude total row from chart
            "datasets": [
                {
                    "values": [row["revenue"] for row in data[:-1]]
                }
            ]
        },
        "type": "donut",
        "height": 300
    }

    # Summary showing the total revenue
    summary = [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green"
        }
    ]

    return columns, data, None, chart, summary
