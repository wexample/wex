from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import KERNEL_RENDER_MODE_CLI


class DataSet2dResponse(AbstractResponse):
    def __init__(self, kernel):
        super().__init__(kernel)

        self.header: list | None = None
        self.body: list | None = None

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
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:
        # Function to adjust the render mode with kernel call method info

        if render_mode == KERNEL_RENDER_MODE_CLI:
            header = self.header if self.header else []  # check for None or empty header
            array = self.body

            # Initialize max widths with zeros
            if header:
                num_columns = len(header)
            else:
                num_columns = len(array[0]) if array else 0  # infer the number of columns from the first row of array
            max_widths = [0] * num_columns

            # Calculate the maximum widths for each column
            for row in array:
                for i, cell in enumerate(row):
                    max_widths[i] = max(max_widths[i], len(str(cell)))

            # Update max widths based on header if exists
            if header:
                for i, cell in enumerate(header):
                    max_widths[i] = max(max_widths[i], len(str(cell)))

            # Calculate the total line length (cell widths + padding + borders)
            total_line_length = sum(max_widths) + (num_columns * 2) + (num_columns - 1)  # padding and separators

            # Generate the horizontal separator line
            separator_line = "+" + "-" * total_line_length + "+\n"

            bash_array = separator_line

            # Add header only if exists
            if header:
                header_str = "|"
                for i, cell in enumerate(header):
                    header_str += f" {cell:<{max_widths[i]}} |"
                bash_array += header_str + "\n"
                bash_array += separator_line

            # Add data rows
            for row in array:
                row_str = "|"
                for i, cell in enumerate(row):
                    row_str += f" {str(cell):<{max_widths[i]}} |"
                bash_array += row_str + "\n"

            bash_array += separator_line

            self.output_bag.append(bash_array)
        return self
