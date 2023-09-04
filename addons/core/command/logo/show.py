from src.helper.string import text_truncate, text_center
from src.helper.core import core_kernel_get_version
from src.const.globals import COLOR_RED, COLOR_RESET, COLOR_LIGHT_GRAY
from src.core.Kernel import Kernel
from src.decorator.command import command


@command()
def core__logo__show(kernel: Kernel) -> str:
    width = 54
    padding = 2

    version_string = f"v{core_kernel_get_version(kernel)}"

    centered = text_center(
        ".o%%%o.\n"
        + ".%%%%%%%%%%%%%%.\n"
        + ".&&&%%%%%%%%%%%%%%%%%%%%%.\n"
        + "&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        + "&&&&&&/    %%%%%%%%%%%%   \\%%%%%%%\n"
        + "&&&&&&     %%%%%%%%%%%%     %%%%%%\n"
        + "&&&&&&     &&&&&%%%%%%%     %%%%%%\n"
        + "&&&&&&     &&&`    `&&&     %%&&&&\n"
        + "&&&&&&./&                &\\.&&&&&&\n"
        + "&&&&&&&&@      .&&.      &&&&&&&&&\n"
        + " &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n"
        + "`&&&&&&&&&&&&&&&&&&&&&&&&`\n"
        + "`&&&&&&&&&&&&&&`\n"
        + "`°&&&&°`\n"
        + f"{COLOR_RESET}\n"
        + ".-..-..-. .--. .-.,-. \n"
        + ": `; `; :' '_.'`.  .'\n"
        + "`.__.__.'`.__.':_,._;\n"
        + "★ www.wexample.com ★\n"
        + f"{version_string}\n\n",
        width
    )

    text = "The software we provide is entirely free and crafted with care by a vibrant, dedicated community. Our " \
           "collective aim is to harness the potential of technology to create tools that can pave the way for a " \
           "brighter future for humanity. As we strive to innovate and improve, we invite you to join us on this " \
           "journey. Visit our website to learn more about our groundbreaking solutions, engage in meaningful " \
           "discussions about technology's potential, and perhaps even consider becoming an active member. Your " \
           "participation and support can significantly enhance our ability to bring about positive change through " \
           "technology. We sincerely hope you will help us shape a better tomorrow."

    return (f"{COLOR_RED}\n\n"
            + centered
            + "\n"
            + f"{COLOR_LIGHT_GRAY}" + text_truncate(text, width, padding) + f"{COLOR_RESET}\n"
            + "\n"
            + "\n")
