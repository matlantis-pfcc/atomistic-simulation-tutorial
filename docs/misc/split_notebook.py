import argparse
import os
import pathlib
import shutil
from typing import Union

import nbformat
from nbformat.notebooknode import NotebookNode
from distutils.util import strtobool

parser = argparse.ArgumentParser()
parser.add_argument("--tutorials-dir", default="tutorials")
parser.add_argument("--tutorials-bilingual-dir", default="tutorials/bilingual")
parser.add_argument("--remove-bilingual-dir", type=strtobool, default="false")
args = parser.parse_args()


def split_notebook(
        notebook: Union[str, pathlib.Path],
        jp_notebook: Union[str, pathlib.Path],
        en_notebook: Union[str, pathlib.Path],
        strict: bool = True,
) -> None:
    # When `strict=True`, all cell must be annotated by [JP], [EN] or [ALL].
    with open(notebook, "r") as f:
        text = f.read().replace("\n", "")
        notebook = nbformat.reads(text, as_version=4)

    JP_cell = []
    EN_cell = []

    for i, cell in enumerate(notebook.cells):
        if cell["cell_type"] == "markdown":
            if cell["source"][:5] == "[EN]\n":
                cell["source"] = cell["source"][5:]
                if cell["source"].startswith("\n"):
                    cell["source"] = cell["source"][1:]
                EN_cell.append(cell)
            elif cell["source"][:5] == "[JP]\n":
                cell["source"] = cell["source"][5:]
                if cell["source"].startswith("\n"):
                    cell["source"] = cell["source"][1:]
                JP_cell.append(cell)
            elif cell["source"][:6] == "[ALL]\n":
                cell["source"] = cell["source"][6:]
                if cell["source"].startswith("\n"):
                    cell["source"] = cell["source"][1:]
                JP_cell.append(cell)
                EN_cell.append(cell)
            else:
                if strict:
                    raise RuntimeError(f"INFO : cannot find language annotation for cell {i}")
                else:
                    print(f"INFO : cannot find language annotation for cell {i}, considered as both JP & EN")
                    JP_cell.append(cell)
                    EN_cell.append(cell)
        else:
            JP_cell.append(cell)
            EN_cell.append(cell)

    if len(JP_cell) != len(EN_cell):
        if strict:
            raise RuntimeError(f"The number of cell is different! JP {len(JP_cell)} != EN {len(EN_cell)}.")
        else:
            print(f"WARNING: the number of cell is different! JP {len(JP_cell)} != EN {len(EN_cell)}.")

    with open(en_notebook, mode="wt") as f:
        EN_nb = NotebookNode(
            {
                "cells": EN_cell,
                "metadata": notebook["metadata"],
                "nbformat": notebook["nbformat"],
                "nbformat_minor": notebook["nbformat_minor"],
            }
        )
        nbformat.write(EN_nb, f)

    with open(jp_notebook, mode="wt") as f:
        JP_nb = NotebookNode(
            {
                "cells": JP_cell,
                "metadata": notebook["metadata"],
                "nbformat": notebook["nbformat"],
                "nbformat_minor": notebook["nbformat_minor"],
            }
        )
        nbformat.write(JP_nb, f)


project_root_dir = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent
tutorials = project_root_dir / args.tutorials_dir
tutorials_bilingual = project_root_dir / args.tutorials_bilingual_dir
print(f"project_root_dir   : {project_root_dir}")
print(f"tutorials          : {tutorials}")
print(f"tutorials_bilingual: {tutorials_bilingual}")
file_names = sorted([f.name.replace("".join(f.suffixes), "") for f in tutorials_bilingual.glob("*.ipynb")])
print(f"file_names: {file_names}")
tutorials_jp = tutorials / "ja"
tutorials_en = tutorials / "en"

tutorials.mkdir(exist_ok=True, parents=True)
tutorials_jp.mkdir(exist_ok=True, parents=True)
tutorials_en.mkdir(exist_ok=True, parents=True)

for f in file_names:
    print(f)
    split_notebook(
        notebook=tutorials_bilingual / f"{f}.ipynb",
        jp_notebook=tutorials_jp / f"{f}.ipynb",
        en_notebook=tutorials_en / f"{f}.ipynb",
    )

# Copy `output` directory
shutil.copytree(tutorials_bilingual / "output", tutorials_jp / "output")
shutil.copytree(tutorials_bilingual / "output", tutorials_en / "output")

if args.remove_bilingual_dir:
    shutil.rmtree(tutorials_bilingual)
