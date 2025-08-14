import pytest
import os
import json
import datetime
import re
import requests
import subprocess
from datetime import timedelta
from playwright.sync_api import sync_playwright
from utils.data_utils import project_path


# ------------------ GLOBALS ------------------ #
RUN_TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
SCREENSHOT_DIR = os.path.join("screenshots", RUN_TIMESTAMP)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

config = {}
playwright = None

# ------------------ CLI OPTIONS ------------------ #
def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="data/config.json")
    parser.addoption(
        "--browsers",
        action="store",
        default=None,
        help="Comma-separated list: chromium,firefox,webkit"
    )
    parser.addoption("--instances", action="store", default="1", help="Instances per browser")
    parser.addoption("--mcp", action="store_true", help="Enable MCP proxy for self-healing")

# ------------------ LOAD CONFIG ------------------ #
def load_config(path='data/config.json'):
    abs_path = project_path(path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Config file not found: {abs_path}")

    with open(abs_path, 'r') as f:
        cfg = json.load(f)

    env_section = cfg.get("environment", {})
    token_var = env_section.get("auth_token_env_var")
    if token_var:
        token = os.getenv(token_var)
        if token:
            env_section["auth_token"] = token
    cfg["environment"] = env_section
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
    config = load_config(request.config.getoption("--config"))
    print("\n[Setup] Starting Playwright...")
    playwright = sync_playwright().start()
    yield
    print("\n[Teardown] Stopping Playwright...")
    playwright.stop()

# ------------------ PAGE FIXTURE ------------------ #
@pytest.fixture
def page(browser_name):
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
    page = context.new_page()
    page.goto(config["environment"]["base_url"], wait_until="load", timeout=30000)
    yield page
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

    if report.when == "call" and report.failed:
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
