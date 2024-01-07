# Import packages
from datetime import datetime, timedelta

# Untuk kembali ke directory utama
import sys
import os
sys.path.insert(
    0, os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..'
        )
    )
)

class DatetimeUtils:
    def formatDatetime(dateStr : str):
        result = datetime.strptime(str(dateStr),'%Y%m%d%H%M')
        return result