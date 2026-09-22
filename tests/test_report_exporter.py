from pathlib import Path

import utils.report_exporter as exporter


def test_report_export(tmp_path):
    exporter.EXPORT_DIR = tmp_path

    result = exporter.export_report(
        query="Pytest rapor testi",
        final_answer=(
            "# Test Raporu\n\n"
            "## Bulgular\n\n"
            "- Birinci bulgu\n"
            "- İkinci bulgu\n\n"
            "## Sonuç\n\n"
            "Test tamamlandı."
        )
    )

    docx_path = Path(
        result["docx_path"]
    )

    pdf_path = Path(
        result["pdf_path"]
    )

    assert docx_path.exists()
    assert pdf_path.exists()

    assert docx_path.suffix == ".docx"
    assert pdf_path.suffix == ".pdf"

    assert docx_path.stat().st_size > 0
    assert pdf_path.stat().st_size > 0