import subprocess, sys, time, re, signal, threading
from pathlib import Path
from pystyle import Colors, Colorate

BOT_FILES = [
    r"A:\Cracked!\main.py",
    r"B:\Buffer0verfl0w\All Project buffer0verfl0w\Project RunV3\main.py",
    r"C:\Buffer0verfl0w\All Project buffer0verfl0w\bot\main.py",
    r"D:\status\index.js",
    r"E:\Buffer0verfl0w\TEst\Node\index.js",
]

MAX_RESTARTS, RESTART_DELAY = 3, 5
RUNNERS = {".py": [sys.executable, "-u"], ".js": ["node"]}
QUOTE = re.compile(r'[\s&()\[\]{}^=;!\'+,`~]')
processes, restart_counts = {}, {}
shutting_down = False

def quote(s):
    return f'"{s}"' if QUOTE.search(s) else s

def logo():
    text = '''
██████╗ ██╗   ██╗███████╗███████╗███████╗██████╗ 
██╔══██╗██║   ██║██╔════╝██╔════╝██╔════╝██╔══██╗ 
██████╔╝██║   ██║█████╗  █████╗  █████╗  ██████╔╝ 
██╔══██╗██║   ██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██╗ 
██████╔╝╚██████╔╝██║     ██║     ███████╗██║  ██║ 
╚═════╝  ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝ 

 ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗      ██████╗ ██╗    ██╗ 
██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║     ██╔═══██╗██║    ██║ 
██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║     ██║   ██║██║ █╗ ██║ 
██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  ██║     ██║   ██║██║███╗██║ 
╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██║     ███████╗╚██████╔╝╚███╔███╔╝ 
 ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ 
'''
    print(Colorate.Horizontal(Colors.rainbow, text))

def start(file):
    path = Path(file).resolve()
    if not path.exists():
        print(f"[ERROR] ไม่พบไฟล์ : {path}")
        return

    runner = RUNNERS.get(path.suffix.lower())
    if not runner:
        print(f"[ERROR] ไม่รองรับไฟล์ : {path.name}")
        return

    title = f"{path.parent.name} - {path.name}"
    cmd = " ".join(quote(x) for x in runner + [path.name])

    return subprocess.Popen(
        ["cmd", "/c", f"title {title} && {cmd}"],
        cwd=path.parent,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def monitor(file):
    restart_counts.setdefault(file, 0)

    while not shutting_down:
        process = start(file)
        if process is None:
            return

        processes[file] = process
        code = process.wait()

        if shutting_down or code == 0:
            return

        restart_counts[file] += 1
        count = restart_counts[file]

        if count > MAX_RESTARTS:
            print(f"[ERROR] '{file}' Crash {MAX_RESTARTS}")
            return

        print(
            f"[WARN] '{file}' Crash ( Code={code} ) — "
            f"restart {count} / {MAX_RESTARTS}"
        )
        time.sleep(RESTART_DELAY)

def shutdown(*_):
    global shutting_down
    if shutting_down:
        return

    shutting_down = True

    for p in processes.values():
        if p.poll() is None:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(p.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

def main():
    logo()
    signal.signal(signal.SIGINT, shutdown)

    threads = [
        threading.Thread(target=monitor, args=(file,), daemon=True)
        for file in BOT_FILES
    ]

    for thread in threads:
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        shutdown()

if __name__ == "__main__":
    main()