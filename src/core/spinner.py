import sys
import threading
import time


class Spinner:
    def __init__(self, message=' ', delay=0.1):
        self.spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.delay = delay
        self.message = message
        self.idx = 0
        self.running = False

    def start(self):
        self.running = True
        sys.stdout.write('\033[?25l')  # Masque le curseur
        threading.Thread(target=self.run).start()

    def run(self):
        while self.running:
            sys.stdout.write('\r' + self.message + self.spinner[self.idx])
            sys.stdout.flush()
            time.sleep(self.delay)
            self.idx = (self.idx + 1) % len(self.spinner)

    def stop(self):
        self.running = False
        time.sleep(self.delay)
        sys.stdout.write('\r' + ' ' * (len(self.message) + len(self.spinner[self.idx]) + 1) + '\r')
        sys.stdout.flush()
        sys.stdout.write('\033[?25h')  # Affiche le curseur
