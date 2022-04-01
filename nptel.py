import typer as t
from typing import Optional
import json

app = t.Typer()


@app.command()
def main(name: Optional[str] = None):
    """
        --name : Send First Name as Argumnet
    """
    msg = "hello"
    if name:
        name = t.style(
            f"{name}", fg=t.colors.BRIGHT_CYAN, bold=True, underline=True)
        t.echo(msg+" " + name)
    else:
        t.secho(msg+" world", fg='blue')


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
    json_object = json.dumps(qbank_json, indent = 4)
    with open(qbank_file+".json","w") as f:
        f.write(json_object)
    
    
if __name__ == "__main__":
    app()
