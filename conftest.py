import pytest
import os
import json
import datetime
import re
import requests
import subprocess
from collections import defaultdict
from datetime import timedelta
from playwright.sync_api import sync_playwright
from utils.data_utils import project_path
from utils.message_utils import send_email_from_config,send_teams_message

# ------------------ GLOBALS ------------------ #
RUN_TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
SCREENSHOT_DIR = os.path.join("screenshots", RUN_TIMESTAMP)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
TEST_RESULTS = defaultdict(int)

config = {}
playwright = None

# ------------------ CLI OPTIONS ------------------ #
def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="data/config.json")
    parser.addoption("--env", action="store", default=None, help="Choose environment/brand (e.g. moes, brandB)")
    parser.addoption(
        "--browsers",
        action="store",
        default=None,
        help="Comma-separated list: chromium,firefox,webkit"
    )
    parser.addoption("--instances", action="store", default="1", help="Instances per browser")
    parser.addoption("--mcp", action="store_true", help="Enable MCP proxy for self-healing")


# ------------------ LOAD CONFIG ------------------ #
def load_config(path='data/config.json', request=None):
    abs_path = project_path(path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Config file not found: {abs_path}")

    with open(abs_path, 'r') as f:
        cfg = json.load(f)

    # ---- Pick environment in priority: --env > ENV var > defaultEnv ----
    env_name = None
    if request:
        env_name = request.config.getoption("--env")
    if not env_name:
        env_name = os.getenv("ENV")
    if not env_name:
        env_name = cfg.get("defaultEnv", "moes")

    environments = cfg.get("environments", {})
    if env_name not in environments:
        raise ValueError(f"Environment '{env_name}' not found in config.json")

    cfg["environment"] = environments[env_name]

    # ---- Handle token injection from OS env vars ----
    token_var = cfg["environment"].get("auth_token_env_var")
    if token_var:
        token = os.getenv(token_var)
        if token:
            cfg["environment"]["auth_token"] = token

    print(f"[INFO] Running tests on environment: {env_name}")
    return cfg

# ------------------ PARAMETRIZE TESTS ------------------ #
def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
        browsers_opt = metafunc.config.getoption("browsers")
        if browsers_opt:
            browsers = [b.strip() for b in browsers_opt.split(",") if b.strip()]
            metafunc.parametrize("browser_name", browsers, scope="session")

# ------------------ SUITE STARTUP ------------------ #
@pytest.fixture(scope="session", autouse=True)
def before_suite(request):
    global playwright, config
    config = load_config(request.config.getoption("--config"), request=request)
    print("\n[Setup] Starting Playwright...")
    playwright = sync_playwright().start()
    yield
    print("\n[Teardown] Stopping Playwright...")
    playwright.stop()


# ------------------ PAGE FIXTURE ------------------ #
@pytest.fixture
def page(browser_name, request):
    default_headless = config.get("headless", True)
    mcp_enabled = config.get("enable_mcp", False)
    proxy_config = {"server": config.get("mcp_proxy", "http://localhost:3000")} if mcp_enabled else None

    args = []
    if browser_name == "chromium":
        args.extend([
            "--disable-infobars",
            "--disable-notifications",
            "--no-default-browser-check",
            "--start-maximized",
            "--window-position=0,0"
        ])
        if mcp_enabled:
            args.append("--proxy-server=http://localhost:3000")

    launch_options = {
        "headless": default_headless,
        "args": args,
    }
    if proxy_config:
        launch_options["proxy"] = proxy_config

    browser = getattr(playwright, browser_name).launch(**launch_options)
    viewport_size = None if browser_name == "chromium" else {"width": 1920, "height": 1080}
    context = browser.new_context(
        accept_downloads=True,
        viewport=viewport_size
    )

    # --- Start tracing ---
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto(config["environment"]["base_url"], wait_until="load", timeout=30000)

    yield page

    # --- Stop tracing and save file ---
    test_name = re.sub(r'[^a-zA-Z0-9_]+', '_', request.node.name)
    trace_dir = os.path.join("reports", "traces")
    os.makedirs(trace_dir, exist_ok=True)
    trace_path = os.path.join(trace_dir, f"{test_name}.zip")
    context.tracing.stop(path=trace_path)
    print(f"[Trace] Saved trace: {trace_path}")

    page.close()
    context.close()
    browser.close()

# ------------------ API SESSION FIXTURE ------------------ #
@pytest.fixture
def api_session():
    session = requests.Session()
    headers = {"Content-Type": "application/json"}
    token = config.get("environment", {}).get("auth_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    session.headers.update(headers)
    return session

# ------------------ SCREENSHOT ON FAILURE ------------------ #
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Count results
        if report.passed:
            TEST_RESULTS["passed"] += 1
        elif report.failed:
            TEST_RESULTS["failed"] += 1
        elif report.skipped:
            TEST_RESULTS["skipped"] += 1

        # Screenshot on failure
        if report.failed:
            page = item.funcargs.get("page", None)
            if page and hasattr(page, "screenshot"):
                try:
                    test_name = re.sub(r'[^a-zA-Z0-9_]+', '_', item.name)
                    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
                    page.screenshot(path=screenshot_path, full_page=True)
                    print(f"\n[Screenshot] Saved: {screenshot_path}")
                except Exception as e:
                    print(f"[WARN] Screenshot capture failed: {e}")
            else:
                print(f"[INFO] No Playwright page object — skipping screenshot for: {item.name}")

# ------------------ POST-SUITE ACTIONS ------------------ #
def pytest_sessionfinish(session, exitstatus):
    print("[Post-Suite] Execution finished.")

    # ------------------ Generate Allure Report ------------------ #
    results_dir = "allure-results"
    if os.path.exists(results_dir) and os.listdir(results_dir):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_dir = os.path.join("reports/allure-report", f"allure-report-{timestamp}")
        os.makedirs(report_dir, exist_ok=True)

        try:
            print("[INFO] Generating Allure HTML report...")
            subprocess.run(
                [
                    r"C:\Users\shiva.ramakrishnan\allure-2.34.1\bin\allure.bat",
                    "generate",
                    results_dir,
                    "--clean",
                    "-o",
                    report_dir
                ],
                check=True,
                shell=True
            )

            print(f"[PASS] Allure report generated at: {report_dir}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to generate Allure report: {e}")
    else:
        print("[WARN] No allure-results found — skipping report generation")

#----------------email&Message-----------------------#


def send_notifications(allure_report_dir):
    # Overall status
    overall_status = "Pass" if TEST_RESULTS["failed"] == 0 else "Fail"

    # Allure summary
    summary = {
        "passed": TEST_RESULTS.get("passed", 0),
        "failed": TEST_RESULTS.get("failed", 0),
        "skipped": TEST_RESULTS.get("skipped", 0)
    }

    # Teams message
    message_text = f"Execution Finished\nPassed: {summary['passed']}\nFailed: {summary['failed']}\nSkipped: {summary['skipped']}\nAllure report attached in email."
    try:
        send_teams_message(message_text)
    except Exception as e:
        print(f"[WARN] Teams message not sent: {e}")

    # Email
    try:
        # zip Allure report for attachment
        import shutil
        zip_path = "reports/allure-report.zip"
        shutil.make_archive("reports/allure-report", 'zip', allure_report_dir)

        send_email_from_config(
            allure_summary=summary,
            overall_status=overall_status
        )
    except Exception as e:
        print(f"[WARN] Email not sent: {e}")
