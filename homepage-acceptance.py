#!/usr/bin/env python3
"""Focused bilingual, responsive and navigation checks for the public Netly site."""
import json
import shutil
import subprocess
import tempfile
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import ProxyHandler, build_opener

import websocket

ROOT = Path(__file__).resolve().parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *_):
        pass


class Browser:
    def __init__(self):
        self.profile = tempfile.mkdtemp(prefix='netly-site-check-')
        executable = shutil.which('google-chrome')
        self.proc = subprocess.Popen([executable, '--headless=new', '--no-sandbox', '--disable-gpu',
            '--disable-dev-shm-usage', '--no-proxy-server', '--remote-debugging-port=0',
            '--remote-allow-origins=*', '--user-data-dir=' + self.profile, 'about:blank'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        active = Path(self.profile) / 'DevToolsActivePort'
        deadline = time.monotonic() + 15
        while not active.exists():
            if self.proc.poll() is not None or time.monotonic() > deadline:
                raise RuntimeError('Chrome failed to start')
            time.sleep(.1)
        port = active.read_text().splitlines()[0]
        targets = json.load(build_opener(ProxyHandler({})).open(f'http://127.0.0.1:{port}/json'))
        self.ws = websocket.create_connection(next(t['webSocketDebuggerUrl'] for t in targets if t['type'] == 'page'),
                                              timeout=10, suppress_origin=True)
        self.sequence = 0
        self.call('Page.enable')
        self.call('Page.addScriptToEvaluateOnNewDocument', {'source':
            'window.acceptanceErrors=[];window.addEventListener("error",e=>window.acceptanceErrors.push(e.message));'})

    def call(self, method, params=None):
        self.sequence += 1
        request_id = self.sequence
        self.ws.send(json.dumps({'id': request_id, 'method': method, 'params': params or {}}))
        while True:
            result = json.loads(self.ws.recv())
            if result.get('id') == request_id:
                if 'error' in result:
                    raise RuntimeError(result['error'])
                return result.get('result', {})

    def js(self, expression):
        result = self.call('Runtime.evaluate', {'expression': expression, 'returnByValue': True, 'awaitPromise': True})
        if 'exceptionDetails' in result:
            raise RuntimeError(result['exceptionDetails'])
        return result.get('result', {}).get('value')

    def wait(self, expression, timeout=10):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.js(expression):
                return
            time.sleep(.1)
        raise AssertionError(f'Timed out: {expression}; title={self.js("document.title")}')

    def close(self):
        self.ws.close()
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    browser = Browser()
    checks = []
    base = f'http://127.0.0.1:{server.server_port}'
    try:
        for page, path in [('home', '/'), ('careers', '/careers.html')]:
            for language in ('en', 'np'):
                for width, height, viewport in [(1440, 1000, 'desktop'), (390, 844, 'mobile')]:
                    browser.call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height,
                        'deviceScaleFactor': 1, 'mobile': viewport == 'mobile'})
                    browser.call('Page.navigate', {'url': f'{base}{path}?lang={language}'})
                    expected = 'ne' if language == 'np' else 'en'
                    browser.wait(f'document.documentElement?.lang === "{expected}" && !!document.querySelector(".language-switch")')
                    assert browser.js('document.querySelectorAll("h1").length === 1'), f'{page}/{language}: expected one page heading'
                    assert browser.js('!!document.querySelector(".skip-link") && !!document.querySelector("nav[aria-label]")'), f'{page}/{language}: missing accessible navigation'
                    assert not browser.js('document.documentElement.scrollWidth > innerWidth + 1'), f'{page}/{language}/{viewport}: horizontal overflow'
                    assert browser.js('Array.from(document.querySelectorAll(".nav-investor")).filter(a => a.href === "https://registry.netly.ai/briefing").length === 1'), f'{page}: investor route mismatch'
                    assert browser.js('Array.from(document.links).filter(a => a.getAttribute("href")?.startsWith("#")).every(a => document.getElementById(a.getAttribute("href").slice(1)))'), f'{page}: broken in-page link'
                    if page == 'home':
                        assert browser.js('document.querySelectorAll(".product-card").length === 3')
                        assert browser.js('document.querySelectorAll(".product-status").length === 3')
                        assert browser.js('Array.from(document.links).some(a => a.getAttribute("href") === "/raqueteer/")')
                        assert browser.js('Array.from(document.links).some(a => a.href.includes("mailto:info@netly.ai?subject=Workflow%20pilot"))')
                        assert browser.js('Array.from(document.links).some(a => a.href.startsWith("https://logbook.netly.ai/simulator/app.html"))')
                        assert browser.js('Array.from(document.links).some(a => a.href === "https://registry.netly.ai/")')
                        if language == 'np':
                            assert browser.js('document.querySelector("#products-title").innerText.includes("यो कार्यशैली")')
                            assert browser.js('document.querySelector(".product-card h3").innerText === "Logbook"')
                        else:
                            assert browser.js('document.querySelector("#products-title").innerText.includes("See how the approach")')
                    else:
                        assert browser.js('document.querySelectorAll(".opening-card").length === 8')
                        assert browser.js('[...document.querySelectorAll(".opening-state")].every(x => x.textContent === (document.documentElement?.lang === "ne" ? "कोषमा निर्भर" : "FUNDING-DEPENDENT"))')
                        assert browser.js('!!document.querySelector(".role-status-note")')
                        if language == 'np':
                            assert browser.js('document.querySelector("#openings-title").innerText.includes("आफूलाई सुहाउने")')
                        else:
                            assert browser.js('document.querySelector("#openings-title").innerText.includes("Find your kind of")')
                    assert browser.js('!(window.acceptanceErrors || []).length'), f'{page}/{language}: uncaught browser error'
                    checks.append(f'{page} · {language} · {viewport}: content, routes, accessibility and layout passed')

        browser.call('Page.navigate', {'url': f'{base}/careers/?lang=np#openings-title'})
        browser.wait('location.pathname === "/careers.html" && location.search === "?lang=np" && location.hash === "#openings-title"')
        browser.wait('document.documentElement?.lang === "ne"')
        checks.append('Careers alias preserves language and anchor through redirect')
        browser.call('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'reduce'}]})
        browser.call('Page.navigate', {'url': f'{base}/?lang=en'})
        browser.wait('!!document.querySelector(".workflow-orbit")')
        assert browser.js('getComputedStyle(document.querySelector(".workflow-orbit")).animationName === "none"')
        browser.call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
        assert browser.js('document.activeElement.matches(".skip-link")')
        checks.append('Reduced-motion and keyboard skip-link checks passed')
        print(json.dumps({'checked_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'checks': checks}, indent=2))
    finally:
        browser.close()
        server.shutdown()


if __name__ == '__main__':
    main()
