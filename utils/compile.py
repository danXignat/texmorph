import os
from pathlib import Path
import subprocess
import platform
import shutil
import time

from utils.dev_tools import compiling_timer


@compiling_timer
def compile_tex(file_path: Path | str, open_pdf: bool = True,
                keep_temp: bool = False, keep_pdf: bool = False,
                output_dir: Path | str | None = None, delete_dellay: float = .5) -> None:
    """
    Compile a LaTeX file and open the resulting PDF.

    Args:
        file_path: Path to the .tex file
        open_pdf: Whether to open the PDF after compilation
        keep_temp: Whether to keep temporary files (.aux, .log, etc.)
        keep_pdf: Whether to keep the PDF file
        output_dir: Directory for output files. If None, uses the same directory as the .tex file
                   Can be absolute or relative to the current working directory.
    """
    # Get absolute paths for everything to avoid confusion
    file_path = Path(file_path).resolve()  # Get absolute path
    original_cwd = Path.cwd().resolve()  # Save original working directory

    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found.")

    if check_pdflatex()[0] == False:
        raise Exception("pdflatex not found. Please install it.")

    file_dir = file_path.parent
    file_name = file_path.stem

    if output_dir is not None:
        output_dir = (original_cwd / Path(output_dir)).resolve()
        os.makedirs(output_dir, exist_ok=True)

        output_arg = ['-output-directory', str(output_dir)]
        pdf_path = output_dir / f"{file_name}.pdf"
    else:
        output_arg = ['-output-directory', str(original_cwd)]
        pdf_path = original_cwd / f"{file_name}.pdf"

    try:
        os.chdir(file_dir)

        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode'] + output_arg + [file_name + ".tex"],
                capture_output=True, text=True, check=False)

            if result.returncode != 0:
                raise Exception(result.stdout)

        except subprocess.CalledProcessError as e:
            error_output = e.stdout if e.stdout else "No error message available."
            raise Exception(f"Compilation failed! Error output: {error_output}")

        if open_pdf and pdf_path.exists():
            open_file(pdf_path)

        if not keep_temp:
            for ext in ['.aux', '.log', '.out', '.toc', '.lof', '.lot']:
                temp_file = Path(output_arg[1]) / f"{file_name}{ext}" if not output_dir else output_dir / f"{file_name}{ext}"
                if temp_file.exists():
                    temp_file.unlink()

        if not keep_pdf and pdf_path.exists():
            time.sleep(delete_dellay)
            pdf_path.unlink()

    finally:
        os.chdir(original_cwd)

def compile_tex_from_string(tex: str, ** kwargs):
    """
    Compiles a LaTeX document provided as a string and handles optional compilation settings.

    This function writes the LaTeX string to a temporary `.tex` file, compiles it using the `compile_tex`
    function, and deletes the temporary file after the compilation process.

    Args:
        tex: The LaTeX document content as a string.
        **kwargs: Additional keyword arguments passed to the `compile_tex` function. These include:
            - open_pdf (bool): Whether to open the generated PDF after compilation (default: True).
            - keep_temp (bool): Whether to keep temporary files (default: False).
            - keep_pdf (bool): Whether to keep the generated PDF file (default: False).
            - output_dir (str | Path | None): The directory where output files should be stored (default: None).
            - delete_dellay (float): Delay in seconds before deleting the generated PDF file (default: 0.5).

    Raises:
        Exception: If there are errors during the compilation process.
    """
    temp = Path("temp.tex")

    with open(temp, "w") as f:
        f.write(tex)

    compile_tex(temp, **kwargs)

    temp.unlink()

def open_file(file_path: Path | str):
    """
    Opens a file specified by the given file path in the default program associated
    with the file type. This function detects the operating system of the executing
    environment and utilizes the appropriate system command to open the file.

    :param file_path: Path to the file to be opened. Accepts a Path object or string.
    :type file_path: Path | str
    """
    match platform.system():
        case 'Darwin':
            subprocess.run(['open', file_path])
        case 'Windows':
            os.startfile(file_path)
        case _:
            subprocess.run(['xdg-open', file_path])

def check_pdflatex():
    """
    Checks the availability of the `pdflatex` executable and its distribution.

    This function determines if the `pdflatex` command is available on the system.
    If available, it checks the version information to identify the LaTeX
    distribution (e.g., MiKTeX, TeX Live, or MacTeX). If the `pdflatex` executable
    is not found, or an error occurs during version checking, the function
    indicates failure.

    :return: A tuple where the first element is a boolean indicating whether the
             `pdflatex` command is available, and the second element is a string
             specifying the detected distribution name or None if unavailable.
    :rtype: tuple[bool, str | None]
    """
    pdflatex_path = shutil.which("pdflatex")
    if pdflatex_path is None:
        return False, None

    try:
        output = subprocess.check_output(["pdflatex", "--version"], text=True)
        output_lower = output.lower()

        match True:
            case _ if "miktex" in output_lower:
                return True, "MiKTeX"
            case _ if "tex live" in output_lower:
                return True, "TeX Live"
            case _ if "mactex" in output_lower:
                return True, "MacTeX"
            case _:
                return True, "Unknown distribution"

    except subprocess.CalledProcessError:
        return False, None

if __name__ == "__main__":
    compile_tex("../data/TEST/test_file.tex")