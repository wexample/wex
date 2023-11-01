import shutil
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import KERNEL_RENDER_MODE_CLI


class DataSet2dResponse(AbstractResponse):
    def __init__(self, kernel):
        super().__init__(kernel)

        self.sections: list = []
        self.current_section = None
        self.new_section()

    def set_title(self, title):
        self.current_section['title'] = title

    def set_header(self, header):
        self.current_section['header'] = header

    def get_header(self):
        return self.current_section['header']

    def set_body(self, body):
        self.current_section['body'] = body

    def get_body(self):
        return self.current_section['body']

    def new_section(self):
        self.current_section = {
            'title': None,
            'header': None,
            'body': None,
        }

        self.sections.append(
            self.current_section
        )

    def render_content(
            self,
            request: CommandRequest,
            render_mode: str = KERNEL_RENDER_MODE_CLI,
            args: dict = None) -> AbstractResponse:
        # Function to adjust the render mode with kernel call method info

        for section in self.sections:
            self.render_content_section(
                section,
                render_mode
            )

        return self

    def render_content_section(
            self,
            section,
            render_mode: str = KERNEL_RENDER_MODE_CLI):

        terminal_size = shutil.get_terminal_size()

        if render_mode == KERNEL_RENDER_MODE_CLI:
            header = section['header'] if section['header'] else []  # check for None or empty header
            array = section['body']
            title = section.get('title', '')

            # Initialize max widths with zeros
            num_columns = len(header) if header else len(array[0]) if array else 0  # infer the number of columns
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

            bash_array = ""

            # Add title if exists, aligned to the left and fill with underscores
            if title:
                # Calculate how much padding is needed on each side of the title
                title_length = len(title)
                padding_each_side = (total_line_length - title_length) // 2

                # Check if we need an extra '=' at the end (for odd width)
                extra_equal = "=" if (total_line_length - title_length) % 2 == 1 else ""

                # Construct the title line
                bash_array += f"{'=' * padding_each_side} {title} {'=' * padding_each_side}{extra_equal}\n"

            bash_array += separator_line

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
