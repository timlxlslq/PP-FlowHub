"""Bounded subprocess capture with live stderr progress delivery."""
import codecs
import os
import selectors
import subprocess
import time


def run_with_progress(command, *, input_text, env, timeout, on_stderr_line):
    started = time.monotonic()
    with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=env) as process:
        selector = selectors.DefaultSelector()
        chunks = {'stdout': [], 'stderr': []}
        decoders = {key: codecs.getincrementaldecoder('utf-8')('replace') for key in chunks}
        pending = ''
        try:
            process.stdin.write(input_text.encode('utf-8'))
            process.stdin.close()
            selector.register(process.stdout, selectors.EVENT_READ, 'stdout')
            selector.register(process.stderr, selectors.EVENT_READ, 'stderr')
            while selector.get_map():
                remaining = timeout - (time.monotonic() - started)
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(command, timeout)
                for key, _ in selector.select(min(remaining, 0.2)):
                    data = os.read(key.fileobj.fileno(), 65536)
                    value = decoders[key.data].decode(data, final=not data)
                    chunks[key.data].append(value)
                    if key.data == 'stderr':
                        pending += value
                        while '\n' in pending:
                            line, pending = pending.split('\n', 1)
                            on_stderr_line(line)
                    if not data:
                        selector.unregister(key.fileobj)
            if pending:
                on_stderr_line(pending)
            process.wait(timeout=max(0.001, timeout - (time.monotonic() - started)))
        except BaseException:
            process.kill()
            process.wait()
            raise
        finally:
            selector.close()
        stdout, stderr = ''.join(chunks['stdout']), ''.join(chunks['stderr'])
        if process.returncode:
            raise subprocess.CalledProcessError(process.returncode, command, stdout, stderr)
        return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
