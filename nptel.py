import json
import random as rnd
import pathlib
import time
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
    clearConsole()
    name = t.style(name, bold=True, fg=t.colors.RED)
    t.echo("\nWelcome "+name +
           "\n----------------------\nYour Quiz Has been started: \n")
    if weekly:
        week_no = 1  # TODO:  delete this line later on
        quiz_db_file = f"week{week_no}.json"
        # no_qus: int = 10
        quiz: dict = {}
        with open(quiz_db_file, "r") as jsonfile:
            quiz = json.load(jsonfile)
        qweek: int = quiz["week"]
        t.secho(
            f"Week : {qweek}\n-----------------------\n", fg=t.colors.YELLOW
        )

        quiz_questions = quiz['qustions']
        rnd.shuffle(quiz_questions)
        # print(quiz_questions)
        total_marks = 0
        attempted_qus = 0
        not_attempted_qus = 10

        with t.progressbar(quiz_questions,label="progress",fill_char=t.style(" ",bg=t.colors.BRIGHT_MAGENTA)) as qq:
            for qus in qq:
                attempted_qus+=1
                not_attempted_qus-=1
                qus_options = qus.get("options")
                rnd.shuffle(qus_options)
                t.echo(f"\n{qus.get('qno')} ) {qus.get('statement')}")

                for i in range(1, 5):
                    t.echo(f"{i}) {qus_options[i-1].get('value')}")

                ans = t.prompt("Select Option no ")

                ans_success = t.colors.RED

                if not (ans>="1" and ans<="4"):
                    t.secho("Please give proper option value; within [1-4]")
                    raise t.Abort()
                else:
                    ans = int(ans)
                if qus_options[ans-1].get("is_correct") == True:
                    ans_success = t.colors.GREEN
                    total_marks += 1

                clearConsole()
                # print qus ans by clearing the previous screen
                t.echo(f"{qus.get('qno')} ) {qus.get('statement')}")
                for i in range(1, 5):
                    time.sleep(.1)
                    if i == ans:
                        # TODO: .value add
                        t.secho(f"{i}) {qus_options[i-1].get('value')}", fg=ans_success)
                    elif qus_options[i-1].get("is_correct") == True:
                        # TODO: .value add
                        t.secho(
                            f"{i}) {qus_options[i-1].get('value')}", fg=t.colors.GREEN)
                    else:
                        t.echo(f"{i}) {qus_options[i-1].get('value')}")
                cnf = t.confirm("Next Qus ",True)
                if not cnf:
                    clearConsole()  
                    print("--------------------------")
                    t.echo(
                        "| Your Result : "+
                        t.style(f"{total_marks}/10",fg=t.colors.BRIGHT_BLUE,bold=True)+
                        "\n| Attempted Qus :"+
                        t.style(f" {attempted_qus} / out of 10",fg=t.colors.BRIGHT_RED)    
                    )
                    print("--------------------------")
                    raise t.Abort()
                clearConsole()
        print("--------------------------")
        t.echo(
            "| Your Result : "+
            t.style(f"{total_marks}/10",fg=t.colors.BRIGHT_BLUE,bold=True)+
            "\n| Attempted Qus :"+
            t.style(f" {attempted_qus} / out of 10",fg=t.colors.BRIGHT_RED)    
        )
        print("--------------------------")

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
