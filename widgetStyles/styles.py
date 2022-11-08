color = "~color~"
mode = "~mode~"
default = "~default~"
button = "~button~"

green = "#9ecd16"
orange = "#FF4400"
light_blue = "#005BC6"
dark_blue = "#051456"

light_grey = "#EFEFEF"
dark_grey = "#222222"

class StatusColor:
    complete = "#00A62E"
    overdue = "#A60000"
    incomplete = "#005BC6"

class ProgressBar:
    red = "#b10000"
    orange = "#D26500"
    yellow = "#d3df00"
    green = "#75c600"
    
VAULT_BUTTON_COLORS = {
    'app': light_blue,
    'crypto': green,
    'general': StatusColor.overdue
}

placeholders = ["~color~", "~mode~", "~default~", "~button~"]