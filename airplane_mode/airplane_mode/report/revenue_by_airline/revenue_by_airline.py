# # Copyright (c) 2024, ashique and contributors
# # For license information, please see license.txt

import frappe
from frappe import _



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

    # Calculate the total revenue separately to avoid adding extra rows
    total_revenue = sum([row["revenue"] for row in data])

    # Donut Chart Data
    chart = {
        "data": {
            "labels": [row["airline"] for row in data],  # Include only airlines
            "datasets": [
                {
                    "values": [row["revenue"] for row in data]
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
