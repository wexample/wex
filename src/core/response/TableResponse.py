from src.core.response.AbstractTerminalSectionResponse import AbstractTerminalSectionResponse
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import KERNEL_RENDER_MODE_TERMINAL, KERNEL_RENDER_MODE_JSON


class TableResponse(AbstractTerminalSectionResponse):
    def __init__(self, kernel, title: str | None = None, body: None | list = None):
        super().__init__(kernel, title)
        self.header = []
        self.body = []

        if body:
            self.set_body(body)

    def set_header(self, header):
        self.header = header

    def get_header(self):
        return self.header

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
            args: dict = None) -> AbstractResponse:
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            # Render the content based on the header and body attributes
            self.render_cli_content()
        elif render_mode == KERNEL_RENDER_MODE_JSON:
            # Render the content in HTTP format
            self.render_http_content()

        return self

    def calculate_max_widths(self, array: list) -> list:
        """
        Calculate the maximum widths for each column based on the array.
        """
        if not array:  # If the array is empty, return an empty list
            return []

        # Find the row with the maximum number of columns
        num_columns = max(len(row) for row in array)

        # Initialize max widths with zeros for each column
        max_widths = [0] * num_columns

        for row in array:
            for i, cell in enumerate(row):
                # Update the max width for each column if current cell is larger
                max_widths[i] = max(max_widths[i], len(str(cell)))

        return max_widths

    def render_cli_content(self):
        if not len(self.header) and not len(self.body):
            self.output_bag.append('')

            return

        # Calculate maximum widths for each column
        max_widths = self.calculate_max_widths(self.header + self.body)

        # Calculate the total line length (cell widths + padding + borders)
        num_columns = len(max_widths)
        total_line_length = sum(max_widths) + (num_columns * 2) + (num_columns - 1)

        # Generate the horizontal separator line
        separator_line = "+" + "-" * total_line_length + "+\n"

        bash_array = ""
        bash_array += self.render_cli_title(self.title, total_line_length + 2)
        bash_array += separator_line

        # Add header only if exists
        if self.header:
            header_str = "|"
            for i, cell in enumerate(self.header):
                header_str += f" {cell:<{max_widths[i]}} |"
            bash_array += header_str + "\n"
            bash_array += separator_line

        # Add data rows
        for row in self.body:
            row_str = "|"
            for i in range(num_columns):  # Use the maximum number of columns based on header or first row
                cell = row[i] if i < len(row) else ''  # Handle missing cells by filling them with an empty string
                row_str += f" {str(cell):<{max_widths[i]}} |"
            bash_array += row_str + "\n"

        bash_array += separator_line

        self.output_bag.append(bash_array)

    def render_http_content(self):
        # Render the content as JSON for HTTP mode
        self.output_bag.append({
            "body": self.body,
            "header": self.header,
            "title": self.title,
        })

    def print(self, render_mode: str, interactive_data: bool = True):
        return self.output_bag[0]
