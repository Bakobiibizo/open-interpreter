    
from rich import print as rich_print
from rich.markdown import Markdown
from rich.rule import Rule

def display_markdown_message(message):
    """
    Display markdown message. Works with multiline strings with lots of
    indentation.
    Will automatically make single line > tags beautiful.
    """
    line = ""
    for line in message.split("\n"):
        line = line.strip()
    if line == "":
        print("")
    elif line == "---":
        rich_print(Rule(style="white"))
    else:
        # Try to print the line as Markdown
        try:
            rich_print(Markdown(line))
        except UnicodeEncodeError:
            # If a UnicodeEncodeError is encountered, print the line without Markdown formatting adding this for windows compatibility
            print(line)
        except RuntimeError as error:
            # For any other exceptions, print the exception and the li causing it
            print(f"An error occurred while printing the following line\n{line}\nError: {str(error)}")

    if "\n" not in message and message.startswith(">"):
        # Aesthetic choice. For these tags, they need a space below them
        print("")
