import time 
import random as rnd
import os
import typer as t


def show_result(attempted_qus:int, total_marks:int, no_qus:int)->None:
    print("--------------------------------------------------------------")
    t.echo(
        "| Your Result : " +
        t.style(f"{total_marks}/{no_qus}", fg=t.colors.BRIGHT_BLUE, bold=True) +
        "\n| Attempted Qus :" +
        t.style(f" {attempted_qus} / out of {no_qus}", fg=t.colors.BRIGHT_RED) +
        "\n| Percentage :" +
        t.style(f" {total_marks/no_qus:.1%}", fg=t.colors.CYAN) +
        "\n| Accuracy :" +
        t.style(f" {total_marks/attempted_qus:.2%}",
                fg=t.colors.BRIGHT_YELLOW)

    )
    print("---------------------------------------------------------------")


def generate_combo()->list[int,int] :
    """
        this generates combination like [1,3],[2,3]
    """
    rnd.seed(time.time())   
    week = rnd.randint(1,9) #TODO: Change 9 -> 12
    qus_num = rnd.randint(1,10)
    combo = [week,qus_num]  
    return combo   


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)