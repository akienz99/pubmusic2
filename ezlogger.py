""" simple logger """
import time


class EzLogger:
    """
    Simple console logger

    Verbosity levels:

    0 -> Don't display any messages
    1 -> Only Errors will be displayed
    2 -> Errors and warnings will be displayed
    3 -> All messages will be displayed
    """

    def __init__(self, verbose_level=3):
        self.verbosity = verbose_level
        self.is_currently_running = False

        self.message_list = []

    def disp_log_entry(self, msg_type, msg_value):
        """
        Displays a log entry in the console
        """

        while self.is_currently_running is True:
            time.sleep(0.05)

        log_message = ""

        self.is_currently_running = True
        if msg_type == "error" and self.verbosity >= 1:
            log_message = "\033[1;31m[error] " + msg_value + "\033[0m"

        elif msg_type == "warning" and self.verbosity >= 2:
            log_message = "\033[1;33m[warning] " + msg_value + "\033[0m"

        elif msg_type == "playlist" and self.verbosity >= 3:
            log_message = "\033[1;32m[playlist] " + msg_value + "\033[0m"

        elif msg_type == "info" and self.verbosity >= 3:
            log_message = "\033[1;34m[info] " + msg_value + "\033[0m"

        elif self.verbosity >= 3:
            log_message = "\033[1;34m[" + msg_type + \
                "] " + msg_value + "\033[0m"

        if log_message != "":
            print(log_message)
            self.message_list.append(log_message)

        self.is_currently_running = False

    # Short calls for different log types -> future

    def error(self, message):
        """
        Displays an error message in the log
        """
        self.disp_log_entry("error", message)

    def warning(self, message):
        """
        Displays an warning message in the log
        """
        self.disp_log_entry("warning", message)

    def playlist(self, message):
        """
        Displays a playlist info in the log
        """
        self.disp_log_entry("playlist", message)

    def info(self, message):
        """
        Displays an info message in the log
        """
        self.disp_log_entry("info", message)

    # getters and setters

    def get_last_message(self):
        """
        Gets the last displayed message
        """
        try:
            return self.message_list[-1]
        except IndexError:
            return ""

    def get_message_list(self):
        """
        Gets a list of all displayed messages
        """
        return self.message_list

    def get_verbosity(self):
        """
        Returns the current verbosity level
        """
        return self.verbosity

    def set_verbosity(self, new_value):
        """
        Sets the verbosity level
        """
        self.verbosity = new_value
