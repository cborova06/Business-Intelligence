# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from unittest.mock import Mock, patch

import frappe
from frappe.tests.utils import FrappeTestCase

from insights.insights.doctype.insights_dashboard_v3.insights_dashboard_v3 import (
    _generate_local_preview_placeholder,
    get_page_preview,
)


class TestInsightsDashboardv3(FrappeTestCase):
    def setUp(self):
        super().setUp()
        self._original_preview_url = getattr(
            frappe.conf, "preview_generator_url", None
        )

    def tearDown(self):
        frappe.conf.preview_generator_url = self._original_preview_url
        super().tearDown()

    def test_get_page_preview_uses_local_placeholder_when_no_service(self):
        frappe.conf.preview_generator_url = None
        content = get_page_preview("https://example.com")

        self.assertIsInstance(content, (bytes, bytearray))
        self.assertGreater(len(content), 0)

    def test_get_page_preview_calls_configured_service(self):
        fake_content = b"fake-jpeg-bytes"
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.content = fake_content

        frappe.conf.preview_generator_url = "http://example.com/preview"

        with patch(
            "insights.insights.doctype.insights_dashboard_v3.insights_dashboard_v3.requests.post",
            return_value=fake_response,
        ) as post:
            result = get_page_preview("https://example.com", headers={"X-Test": "1"})

        self.assertEqual(result, fake_content)
        post.assert_called_once()

    def test_get_page_preview_falls_back_to_placeholder_on_service_error(self):
        frappe.conf.preview_generator_url = "http://example.com/preview"

        with patch(
            "insights.insights.doctype.insights_dashboard_v3.insights_dashboard_v3.requests.post",
            side_effect=Exception("boom"),
        ):
            content = get_page_preview("https://example.com")

        self.assertIsInstance(content, (bytes, bytearray))
        self.assertGreater(len(content), 0)

    def test_generate_local_preview_placeholder_returns_non_empty_bytes(self):
        content = _generate_local_preview_placeholder()
        self.assertIsInstance(content, (bytes, bytearray))
        self.assertGreater(len(content), 0)
