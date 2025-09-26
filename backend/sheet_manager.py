import gspread
from gspread_formatting import format_cell_ranges, DataValidationRule, BooleanCondition, CellFormat, Color, set_row_height, set_column_width, set_frozen
from oauth2client.service_account import ServiceAccountCredentials

class SheetManager:
    def __init__(self, creds_path, spreadsheet_name):
        self.creds_path = creds_path
        self.spreadsheet_name = spreadsheet_name
        self.client = self._authorize_gspread()
        self.spreadsheet = self._open_spreadsheet()

    def _authorize_gspread(self):
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_path, scope)
            return gspread.authorize(creds)
        except Exception as e:
            print(f"Error authorizing gspread: {e}")
            return None

    def _open_spreadsheet(self):
        if not self.client:
            return None
        try:
            return self.client.open(self.spreadsheet_name)
        except Exception as e:
            print(f"Error opening spreadsheet '{self.spreadsheet_name}': {e}")
            return None

    def create_session_sheet(self, session_name):
        if not self.spreadsheet:
            print("Spreadsheet not available to create new sheet.")
            return None
        try:
            # Check if sheet already exists
            try:
                worksheet = self.spreadsheet.worksheet(session_name)
                print(f"Worksheet '{session_name}' already exists.")
                return worksheet
            except gspread.exceptions.WorksheetNotFound:
                pass # Sheet does not exist, proceed to create

            worksheet = self.spreadsheet.add_worksheet(title=session_name, rows="100", cols="20")
            headers = ["Student Name", "Roll No", "Date", "Time"]
            worksheet.append_row(headers)

            # Basic formatting for headers
            # set_row_format(worksheet, 1, text_format(bold=True)) # This function doesn't exist directly
            set_frozen(worksheet, rows=1)
            format_cell_ranges(worksheet, [
                ('A1:D1', CellFormat(textFormat={'bold': True}))
            ])
            set_column_width(worksheet, 'A', 200)
            set_column_width(worksheet, 'B', 100)
            set_column_width(worksheet, 'C', 120) # Adjusted width for Date
            set_column_width(worksheet, 'D', 100) # Adjusted width for Time

            print(f"Created new worksheet: {session_name}")
            return worksheet
        except Exception as e:
            print(f"Error creating session sheet '{session_name}': {e}")
            return None

    def record_attendance(self, session_name, student_name, roll_number, timestamp):
        """
        Records attendance for a student in a specific session sheet.
        Prevents duplicate submissions for the same student within the same session.
        Returns (success_status, is_duplicate, sessions_attended) where sessions_attended is always 1 for new, 0 for duplicate.
        """
        if not self.spreadsheet:
            print("Spreadsheet not available to record attendance.")
            return False, False, 0 # success, is_duplicate, sessions_attended

        try:
            worksheet = self.spreadsheet.worksheet(session_name)
            all_data = worksheet.get_all_values() # Get all values including header for row index
            headers = all_data[0]
            records = all_data[1:] # Actual data rows

            # Split timestamp into date and time
            attendance_date = timestamp.split(" ")[0]
            attendance_time = timestamp.split(" ")[1]

            # Check for duplicate attendance for the same student in the same session
            for i, row in enumerate(records):
                if len(row) >= 2 and row[0] == student_name and row[1] == roll_number:
                    # Student found, this is a duplicate submission for this session
                    print(f"Duplicate attendance for {student_name} in {session_name}. Already recorded.")
                    return True, True, 0 # success, is_duplicate, sessions_attended (0 for duplicate)

            # If student not found for this session, add new record
            worksheet.append_row([student_name, roll_number, attendance_date, attendance_time])
            print(f"Recorded new attendance for {student_name} in {session_name}. Date: {attendance_date}, Time: {attendance_time}")
            return True, False, 1 # success, is_duplicate, sessions_attended (1 for new)

        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet '{session_name}' not found for attendance recording.")
            return False, False, 0
        except Exception as e:
            print(f"Error recording attendance in '{session_name}': {e}")
            return False, False, 0
