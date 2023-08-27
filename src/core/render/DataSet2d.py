DATASET_RENDER_MODE_CLI = 'cli'


class DataSet2d:
    header: list
    body: list

    def __init__(self):
        pass

    def set_header(self, header):
        self.header = header

    def get_header(self):
        return self.header

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def render(self, kernel, render_mode: str = DATASET_RENDER_MODE_CLI):
        # We'll adjust render mode with kernel call method info

        if render_mode == DATASET_RENDER_MODE_CLI:
            header = self.header
            array = self.body

            # Calculate the maximum widths for each column
            num_columns = len(header)
            max_widths = [0] * num_columns

            for row in array:
                for i, cell in enumerate(row):
                    max_widths[i] = max(max_widths[i], len(str(cell)))

            # Update max widths based on header if necessary
            for i, cell in enumerate(header):
                max_widths[i] = max(max_widths[i], len(str(cell)))

            # Calculate the total line length (cell widths + padding + borders)
            total_line_length = sum(max_widths) + (num_columns * 3) + (num_columns - 1)  # padding and separators

            # Generate the horizontal separator line
            separator_line = "+" + "-" * (total_line_length) + "+\n"

            bash_array = separator_line

            # Add header
            header_str = "|"
            for i, cell in enumerate(header):
                header_str += f"  {cell:<{max_widths[i]}} |"
            bash_array += header_str + "\n"
            bash_array += separator_line

            # Add data rows
            for row in array:
                row_str = "|"
                for i, cell in enumerate(row):
                    row_str += f"  {str(cell):<{max_widths[i]}} |"
                bash_array += row_str + "\n"

            bash_array += separator_line
            return bash_array
