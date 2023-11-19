import os

from src.helper.string import string_truncate, string_multiline_center
from src.helper.core import core_kernel_get_version
from src.const.globals import COLOR_RED, COLOR_RESET, COLOR_LIGHT_GRAY
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.alias import alias


@alias('logo')
@command(help="Show maintainers logo")
def core__logo__show(kernel: Kernel) -> str:
    width = 54
    padding = 2

    version_string = f"v{core_kernel_get_version(kernel)}"

    centered = string_multiline_center(
        ".o%%%o." + os.linesep
        + ".%%%%%%%%%%%%%%." + os.linesep
        + ".&&&%%%%%%%%%%%%%%%%%%%%%." + os.linesep
        + "&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%" + os.linesep
        + "&&&&&&/    %%%%%%%%%%%%   \\%%%%%%%" + os.linesep
        + "&&&&&&     %%%%%%%%%%%%     %%%%%%" + os.linesep
        + "&&&&&&     &&&&&%%%%%%%     %%%%%%" + os.linesep
        + "&&&&&&     &&&`    `&&&     %%&&&&" + os.linesep
        + "&&&&&&./&                &\\.&&&&&&" + os.linesep
        + "&&&&&&&&@      .&&.      &&&&&&&&&" + os.linesep
        + " &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" + os.linesep
        + "`&&&&&&&&&&&&&&&&&&&&&&&&`" + os.linesep
        + "`&&&&&&&&&&&&&&`" + os.linesep
        + "`°&&&&°`" + os.linesep
        + f"{COLOR_RESET}" + os.linesep
        + ".-..-..--. .--. .-.,-." + os.linesep
        + ": `; `;  :' '_.'`.  .'" + os.linesep
        + "`.__.__._'`.__.':_,._;" + os.linesep
        + "★ www.wexample.com ★" + os.linesep
        + f"{version_string}" + os.linesep + os.linesep,
        width
    )

    text = "The software we provide is entirely free and crafted with care by a vibrant, dedicated community. Our " \
           "collective aim is to harness the potential of technology to create tools that can pave the way for a " \
           "brighter future for humanity. As we strive to innovate and improve, we invite you to join us on this " \
           "journey. Visit our website to learn more about our groundbreaking solutions, engage in meaningful " \
           "discussions about technology's potential, and perhaps even consider becoming an active member. Your " \
           "participation and support can significantly enhance our ability to bring about positive change through " \
           "technology. We sincerely hope you will help us shape a better tomorrow."

    return (f"{COLOR_RED}"
            + os.linesep
            + os.linesep
            + centered
            + os.linesep
            + f"{COLOR_LIGHT_GRAY}" + string_truncate(text, width, padding) + f"{COLOR_RESET}{os.linesep}"
            + os.linesep
            + os.linesep)
