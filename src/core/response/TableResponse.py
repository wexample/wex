import os
from typing import TYPE_CHECKING, Any, List, Optional

from src.const.globals import KERNEL_RENDER_MODE_JSON, KERNEL_RENDER_MODE_TERMINAL
from src.const.types import (
    BasicInlineValue,
    OptionalCoreCommandArgsDict,
    ResponsePrintType,
    StringsList,
)
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.AbstractTerminalSectionResponse import (
    AbstractTerminalSectionResponse,
)

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

TableBodyLine = List[BasicInlineValue]
TableBody = List[TableBodyLine]


class TableResponse(AbstractTerminalSectionResponse):
    def __init__(
        self,
        kernel: "Kernel",
        title: str | None = None,
        body: Optional[TableBody] = None,
    ) -> None:
        super().__init__(kernel, title)
        self._header: StringsList = []
        self._body: TableBody = []

        if body:
            self.set_body(body)

    def set_header(self, header: StringsList) -> None:
        self._header = header

    def get_header(self) -> StringsList:
        return self._header

    def set_body(self, body: TableBody) -> None:
        self._body = body

    def get_body(self) -> TableBody:
        return self._body

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            # Render the content based on the header and body attributes
            self.render_cli_content()
        elif render_mode == KERNEL_RENDER_MODE_JSON:
            # Render the content in HTTP format
            self.render_http_content()

        return self

    def calculate_max_widths(self, array: StringsList) -> List[int]:
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

    def render_cli_content(self) -> None:
        combined_list: List[Any] = [self._header] + self._body

        if not len(combined_list):
            self.output_bag.append("")

            return None

        # Calculate maximum widths for each column
        max_widths = self.calculate_max_widths(combined_list)

        # Calculate the total line length (cell widths + padding + borders)
        num_columns = len(max_widths)
        total_line_length = sum(max_widths) + (num_columns * 2) + (num_columns - 1)

        # Generate the horizontal separator line
        separator_line = "+" + "-" * total_line_length + "+" + os.linesep

        bash_array = ""
        bash_array += self.render_cli_title(total_line_length + 2)
        bash_array += separator_line

        # Add header only if exists
        if self._header:
            header_str = "|"
            for i, cell in enumerate(self._header):
                header_str += f" {cell:<{max_widths[i]}} |"
            bash_array += header_str + os.linesep
            bash_array += separator_line

        # Add data rows
        for row in self._body:
            row_str = "|"
            for i in range(
                num_columns
            ):  # Use the maximum number of columns based on header or first row
                cell_content = row[i] if i < len(row) else ""
                # Handle missing cells by filling them with an empty string
                cell_str: str = str(cell_content)
                row_str += f" {cell_str:<{max_widths[i]}} |"
            bash_array += row_str + os.linesep

        bash_array += separator_line

        self.output_bag.append(bash_array)

    def render_http_content(self) -> None:
        # Render the content as JSON for HTTP mode
        self.output_bag.append(
            {
                "body": self._body,
                "header": self._header,
                "title": self.title,
            }
        )

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        return self.get_first_output_printable_value()
