import time
import datetime
import openpyxl
import os
from utils.logger_utils import get_logger

logger = get_logger()


def log_step(step_name, status, test_results, start_time):
    """
    Log a test step with elapsed time and assertion.
    """
    elapsed = round(time.time() - start_time, 2)
    logger.info(f"[{elapsed}s] {step_name} - {status}")
    test_results.append([elapsed, step_name, status])

    # Assertion for FAIL steps
    assert status == "PASS", f"Step failed: {step_name}"


def save_results_to_excel(test_results, filename_prefix="test_results"):
    """
    Save test results into an Excel file with worker name and timestamp.
    Works with pytest-xdist (parallel) and normal single-run.
    """
    # Get worker name from pytest-xdist if available
    worker_name = os.getenv("PYTEST_XDIST_WORKER", "gw0")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{worker_name}_{timestamp}.xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Results"

    # Header
    ws.append(["Time (s)", "Step", "Status"])

    # Write rows
    for row in test_results:
        ws.append(row)

    file_path = os.path.join(os.getcwd(), filename)
    wb.save(file_path)
    logger.info(f"Test results saved to {file_path}")
    return file_path
