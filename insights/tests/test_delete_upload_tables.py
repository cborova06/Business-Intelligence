import frappe
from frappe.tests.utils import FrappeTestCase


class TestDeleteUploadTables(FrappeTestCase):
    def setUp(self):
        super().setUp()
        frappe.set_user("Administrator")

    def test_delete_upload_tables_removes_metadata_for_uploads(self):
        from insights import api as insights_api
        from insights.insights.doctype.insights_table_v3.insights_table_v3 import (
            InsightsTablev3,
        )

        # Ensure uploads data source exists
        if not frappe.db.exists("Insights Data Source v3", "uploads"):
            ds = frappe.get_doc(
                {
                    "doctype": "Insights Data Source v3",
                    "name": "uploads",
                    "title": "Uploads",
                    "database_type": "DuckDB",
                    "database_name": "insights_file_uploads_test",
                    "status": "Active",
                }
            )
            ds.insert()

        table_name = "tmp_delete_me"

        # Create metadata row for uploads table
        InsightsTablev3.bulk_create("uploads", [table_name])

        exists_before = frappe.get_all(
            "Insights Table v3",
            filters={"data_source": "uploads", "table": table_name},
            pluck="name",
        )
        self.assertTrue(exists_before)

        # Call delete_upload_tables
        insights_api.delete_upload_tables([table_name])

        # Metadata should be gone
        exists_after = frappe.get_all(
            "Insights Table v3",
            filters={"data_source": "uploads", "table": table_name},
            pluck="name",
        )
        self.assertFalse(exists_after)
