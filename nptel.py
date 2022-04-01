import json
import pathlib
from typing import Optional

import typer as t

BASEDIR = pathlib.Path().absolute()

app = t.Typer()


@app.command()
def startquiz_by_week(
    name: str = t.Option("Hola", prompt="Write Your Name"),
    week: str = t.Option("1", help="by default 1",prompt="week # : ")
    
):
    t.echo(name+" "+week)


@app.command()
def addqus(
    week: int = t.Option(..., min=1, max=12)
):
    """
        Per week 10 qustions will be taken input via cmd
        & per qus 4 options will be added
        --week: Week No
    """
    qbank_file = "week"+str(week)
    no_options = 4
    noq = 10
    questions = []
    options = []
    readlines = []
    qbank_json = {
        "week": week
    }
    with open(qbank_file+".txt", "r") as file:
        readlines = file.readlines()

    for index in range(noq):
        qstatement = readlines.pop(0).rstrip("\n")
        options = readlines[:4]
        ans = readlines[4]
        options = [
            {
                "value": op.rstrip("\n"),
                "is_correct": op.rstrip("\n") == ans.rstrip("\n")
            } for op in options
        ]
        for _ in range(no_options+1):
            readlines.pop(0)

        questions.append(
            {
                'qno': index+1,
                "statement": qstatement,
                "options": options
            }
        )
    qbank_json["qustions"] = questions
    json_object = json.dumps(qbank_json, indent=4)
    with open(qbank_file+".json", "w") as f:
        f.write(json_object)
    success_msg = f"| Your "+t.style(f"week{week}.txt", fg=t.colors.BRIGHT_RED)+" has been successfuly converted to "+t.style(
        f"week{week}.json", fg=t.colors.GREEN, bold=True)
    qbank_json_file = qbank_file+".json"
    t.echo(
        "\n-----------------------------------------------------------------\n" +
        success_msg +
        "\n| file saved in location ->  " +
        t.style(f"{BASEDIR/qbank_json_file}", fg=t.colors.BRIGHT_CYAN) +
        "\n-----------------------------------------------------------------\n"
    )


if __name__ == "__main__":
    app()
