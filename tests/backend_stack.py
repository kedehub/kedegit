"""Shared seed-selected KEDEHub launcher for KEDEGit integration tests."""
import json
import os
import queue
import shutil
import socket
import platform
import subprocess
import tempfile
import threading
import time
from pathlib import Path

import yaml


class BackendStack:
    def __init__(self, config_dir):
        self.runtime = tempfile.TemporaryDirectory(prefix='kedehub-playwright-')
        (Path(self.runtime.name) / 'owner.json').write_text(json.dumps({'hostname': platform.node(), 'pid': os.getpid()}))
        self.process = None
        self._config_dir = Path(config_dir)
        self._previous_env = os.environ.get('KEDEGITDIR')
        try:
            root = Path(os.environ.get('KEDEHUB_SERVER_PATH',
                        Path(__file__).resolve().parents[2] / 'kedehub_server')).resolve()
            python = os.environ.get('KEDEHUB_SERVER_PYTHON')
            if not python:
                for candidate in ('venv311/bin/python', 'venv311/bin/python3', '.venv/bin/python'):
                    executable = root / candidate
                    if executable.exists() and subprocess.run(
                            [str(executable), '-c', 'import uvicorn'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                        python = str(executable)
                        break
            python = python or shutil.which('python3') or 'python3'
            with socket.socket() as listener:
                listener.bind(('127.0.0.1', 0))
                self.port = listener.getsockname()[1]
            self.process = subprocess.Popen([
                python, str(root / 'tests/e2e/run_temp_db_server.py'),
                '--seed', 'test-company', '--port', str(self.port),
                '--runtime-dir', self.runtime.name, '--exit-on-stdin-eof'
            ], cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                text=True, bufsize=1)
            lines = queue.Queue()
            ready = threading.Event()

            def drain():
                for line in self.process.stdout:
                    if not ready.is_set():
                        lines.put(line)
                lines.put(None)

            self._reader = threading.Thread(target=drain, daemon=True)
            self._reader.start()
            deadline = time.monotonic() + 60
            while True:
                try:
                    line = lines.get(timeout=max(0, deadline - time.monotonic()))
                except queue.Empty:
                    raise RuntimeError('Timed out waiting for KEDEHub readiness')
                if line is None:
                    raise RuntimeError('KEDEHub exited before readiness')
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get('event') != 'kedehub-e2e-token':
                    continue
                if event.get('seed') != 'test-company' or not isinstance(event.get('token'), str) or not event['token']:
                    raise RuntimeError('Invalid test-company readiness event')
                ready.set()
                self.token = event['token']
                break
            self._config_dir.mkdir(parents=True, exist_ok=True)
            config = self._config_dir / 'config.yaml'
            data = yaml.safe_load(config.read_text()) if config.exists() else {}
            data = data or {}
            data['server'] = dict(protocol='http', host='127.0.0.1', port=self.port)
            data['company'] = dict(name='test_company', user='af9b995c-956e-49ad-a6ac-26a72613f075', token=self.token)
            config.write_text(yaml.safe_dump(data))
            os.environ['KEDEGITDIR'] = str(self._config_dir)
            # Consumers retain this configuration object and cache their clients.
            # Reload it in place before switching to a fresh backend/port.
            from kedehub import server_config
            from kedehub_client import get_client, get_sync_apis, get_async_apis
            server_config.config.clear()
            server_config.set_file(str(config))
            get_sync_apis.cache_clear()
            get_async_apis.cache_clear()
            get_client.cache_clear()
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.process is not None:
            self.process.stdin.close()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)
            if hasattr(self, '_reader'):
                self._reader.join(timeout=2)
            self.process.stdout.close()
            self.process = None
        self.runtime.cleanup()
        if self._previous_env is None:
            os.environ.pop('KEDEGITDIR', None)
        else:
            os.environ['KEDEGITDIR'] = self._previous_env
