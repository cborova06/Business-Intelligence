import unittest

import frappe
import ibis

from frappe.exceptions import ValidationError

from insights.insights.doctype.insights_data_source_v3.ibis_utils import (
    IbisQueryBuilder,
)


class TestIbisUtilsEvaluateExpression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Basit bir Insights Query v3 dokümanı simüle edip
        # üzerinde mutate çalıştırabileceğimiz bir ibis tablosu oluşturuyoruz.
        from insights.insights.doctype.insights_data_source_v3.insights_data_source_v3 import (
            InsightsDataSourcev3,
        )
        from insights.insights.doctype.insights_query_v3.insights_query_v3 import (
            InsightsQueryv3,
        )

        # Kullanılabilir bir data source varsayımı ile basit bir query dokümanı yarat
        ds = frappe.get_all("Insights Data Source v3", limit=1)
        if not ds:
            # test ortamında en az bir data source yoksa oluştur
            source = frappe.get_doc(
                {
                    "doctype": "Insights Data Source v3",
                    "title": "Test Data Source",
                    "database_type": "DuckDB",
                    "database_name": "test_ibis_utils",
                }
            ).insert()
        else:
            source = frappe.get_doc("Insights Data Source v3", ds[0].name)

        query = frappe.get_doc(
            {
                "doctype": "Insights Query v3",
                "title": "Test Expression Query",
                "data_source": source.name,
                "operations": [],
            }
        ).insert()

        # Basit bir in‑memory DuckDB tablosu (columns: Price, Discount)
        # Not: Burada sadece şema bizim için önemli.
        cls.price_column_name = "Price"
        cls.discount_column_name = "Discount"

        # IbisQueryBuilder, perform_operation ile mutate içinde evaluate_expression'i çağırıyor.
        cls.query_doc = query

    def _build_builder_with_schema(self):
        """
        evaluate_expression, self.query.schema().names üzerinden
        kolonları okuyor. Basit bir ibis tablosu ile bunu simüle ediyoruz.
        """
        builder = IbisQueryBuilder(self.query_doc)
        # Price ve Discount isimli kolonlara sahip sahte bir tablo oluştur.
        self.assertIsNone(getattr(builder, "query", None))
        schema = ibis.schema(
            {self.price_column_name: "float64", self.discount_column_name: "float64"}
        )
        builder.query = ibis.table(schema=schema, name="t")
        return builder

    def test_valid_expression_returns_ibis_expr(self):
        """Geçerli bir ifade evaluate_expression ile başarıyla derlenmeli."""
        builder = self._build_builder_with_schema()
        expr = f"{self.price_column_name} * (1 - {self.discount_column_name} / 100)"

        result = builder.evaluate_expression(expr)

        # Sonucun bir ibis Expression olduğunu doğrula
        from ibis.expr.types import Expr

        self.assertIsInstance(result, Expr)

    def test_name_error_raises_validation_with_column_list(self):
        """Tanımsız kolon kullanılırsa kullanıcı dostu bir ValidationError fırlatılmalı."""
        builder = self._build_builder_with_schema()
        # 'WrongColumn' mevcut değil, NameError tetiklemeli
        expr = "WrongColumn * 2"

        with self.assertRaises(ValidationError) as ctx:
            builder.evaluate_expression(expr)

        msg = str(ctx.exception)
        self.assertIn("Column 'WrongColumn' is not defined in this query", msg)
        # Kullanılabilir kolonların listesi mesajda geçiyor olmalı
        self.assertIn(self.price_column_name, msg)
        self.assertIn(self.discount_column_name, msg)

    def test_syntax_error_raises_validation_with_friendly_message(self):
        """Python sentaks hataları kullanıcı dostu bir mesajla aktarılmalı."""
        builder = self._build_builder_with_schema()
        # Geçersiz Python ifadesi
        expr = "Price (Rs.)*(Discount (%)/100)"

        with self.assertRaises(ValidationError) as ctx:
            builder.evaluate_expression(expr)

        msg = str(ctx.exception)
        self.assertIn("Invalid expression syntax", msg)

    def test_empty_expression_raises_value_error(self):
        """Boş ifade ValueError ile reddedilmeli."""
        builder = self._build_builder_with_schema()

        with self.assertRaises(ValueError):
            builder.evaluate_expression(" ")

