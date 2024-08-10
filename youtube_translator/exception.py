import sys
import traceback
from youtube_translator.logger import logging


def format_error_message(error, error_detail: sys):
    """Formats detailed error message with file name, line number, and error."""
    exc_type, exc_value, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = (
        f"Error occurred while processing file: {file_name}\n"
        f"Line number: {line_number}\n"
        f"Error: {str(error)}"
    )
    return error_message


class YoutubeException(Exception):
    """Custom exception class for handling errors in QnA systems."""

    def __init__(self, error_message, error_detail: sys):
        """
        Initialize QnAException with a formatted error message.

        :param error_message: The original error message.
        :param error_detail: The sys module for error details.
        """
        super().__init__(error_message)
        self.error_message = format_error_message(error_message, error_detail)

    def __str__(self):
        return self.error_message


# Example usage
if __name__ == '__main__':
    try:
        # Example code that raises an exception
        result = 3 / 0
    except Exception as e:
        logging.error(e, exc_info=True)
        raise YoutubeException(str(e), sys)
