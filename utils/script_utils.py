import time
import datetime
import inspect
import openpyxl
from pathlib import Path
import os
from utils.logger_utils import get_logger

logger = get_logger()


def log_step(step_name, status, test_results, start_time, order_id="", order_time="", browser_name="browser"):
    """
    Logs a test step, stores it in test_results, and optionally saves Excel at the end.
    """
    elapsed = round(time.time() - start_time, 2)
    logger.info(f"[{elapsed}s] {step_name} - {status}")

    # Append as a list for Excel
    test_results.append([elapsed, step_name, status, order_id, order_time])

    # Fail immediately if step fails
    if status != "PASS":
        # Save results automatically if failed
        save_results_to_excel(
            test_results,
            browser_name=browser_name,
            test_case_name=inspect.currentframe().f_back.f_back.f_code.co_name
        )
        assert status == "PASS", f"Step failed: {step_name}"


def save_results_to_excel(test_results, browser_name="browser", test_case_name=None):
    """
    Save test results dynamically with format:
    {test_name}_{browser}_{YYYYMMDD_HHMMSS}.xlsx
    """
    results_folder = Path(os.getcwd()) / "Assertion_result"
    results_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Infer test case name if not provided
    if not test_case_name:
        test_case_name = inspect.currentframe().f_back.f_back.f_code.co_name

    filename = f"{test_case_name}_{browser_name}_{timestamp}.xlsx"
    file_path = results_folder / filename

    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Test Results"

        ws.append(["Time (s)", "Step", "Status", "Order ID", "Order Time"])

        for row in test_results:
            ws.append(row)

        wb.save(file_path)
        logger.info(f"Results saved to: {file_path}")
    except Exception as e:
        logger.exception(f"Failed to save results: {e}")