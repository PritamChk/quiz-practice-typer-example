import json
import random as rnd
import pathlib
import typer as t
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

BASEDIR = pathlib.Path().absolute()

app = t.Typer()


@app.command()
def startquiz(
        name: str = t.Option("Hola", prompt="Write Your Name"),
        week_no: int = t.Option(rnd.randint(1, 12), "-n", min=1, max=12,
                                help="by default 1 and range  [ 1<=x<=12 ]"),
        weekly: bool = t.Option(
            True, "-w", help="If True then qus given weekly else taken randomly from any week"),
        no_qus: int = t.Option(10, "-q", min=3, max=120,
                               help="This is applicable for Random Quiz")
):

    name = t.style(name, bold=True, fg=t.colors.RED)
    t.echo("\nWelcome "+name +
           "\n----------------------\nYour Quiz Has been started: \n")
    if weekly:
        week_no = 1  # TODO:  delete this line later on
        quiz_db_file = f"week{week_no}.json"
        no_qus: int = 10
        quiz: dict = {}
        with open(quiz_db_file, "r") as jsonfile:
            quiz = json.load(jsonfile)
        qweek: int = quiz["week"]
        t.secho(
            f"Week : {week_no}\n-----------------------\n"
        )

        quiz_questions: list[dict] = rnd.shuffle(quiz['questions'])

        total_marks = 0

        for qus in quiz_questions:
            qus_options = rnd.shuffle(qus.get("options"))

            t.echo(qus.get("qno")+") "+qus.get("statement"))

            for i in range(1, 5):
                t.echo(f"{i}) f{qus_options[i-1]}")

            ans = t.prompt("Select Option no: ")
            
            ans_success = lambda ans: t.colors.BRIGHT_GREEN if qus_options[ans].get("is_correct") == True else t.colors.RED

            if ans not in range(1, 5):
                t.secho("Please give proper option value; within [1-4]")
                t.Abort()
            if qus_options[ans].get("is_correct") == True:
                total_marks += 1

            clearConsole()
            #print qus ans by clearing the previous screen
            t.echo(qus.get("qno")+") "+qus.get("statement"))
            for i in range(1, 5):
                if i==ans:
                    t.secho(f"{i}) f{qus_options[i-1]}",fg = ans_success(ans)) #TODO: .value add
                if 

@app.command()
def addqus(
    week: int = t.Option(..., "-w", min=1, max=12,
                         help="Provide the week no and week#.txt should exist in same directory"),
    noq: int = t.Option(10, "-n", min=1, max=10,
                        help="Enter No of Qus to be converted",)
):
    """
        Per week 10 qustions will be taken input via file: week#.txt

        & per qus 4 options will be added

        After that the ans options have to be added

        ## NB: Case sensitive comparisions

        example:

        ---------

        who are you?

        Human

        Yeti

        Dog

        Cat

        Human


        -w : week no for short notation

        -n : no of qus short notation
    """
    qbank_file = "week"+str(week)
    no_options = 4
    # noq = 10
    questions = []
    options = []
    readlines = []
    qbank_json = {
        "week": week
    }
    with open(qbank_file+".txt", "r") as file:
        readlines = file.readlines()

    import time
    label = t.style("Convertion", fg=t.colors.GREEN)
    fchar = t.style(" ", bg=t.colors.GREEN)
    t.echo("")
    with t.progressbar(range(noq), fill_char=fchar, label=label) as noqs:
        for index in noqs:
            time.sleep(.03)
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
