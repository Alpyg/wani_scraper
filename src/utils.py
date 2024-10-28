COLOR = {
    "radical": "#4193F1",
    "kanji": "#EB417D",
    "vocabulary": "#FFFFFF",
    "reading": "#AAAAAA",
}


def get_level_difficulty(level):
    match level:
        case level if level < 11:
            return "pleasant"
        case level if level < 21:
            return "painful"
        case level if level < 31:
            return "death"
        case level if level < 41:
            return "hell"
        case level if level < 51:
            return "paradise"
        case _:
            return "reality"


def annotate(string):
    return (
        string.replace(
            '<mark title="Radical" class="radical-highlight">',
            f'<font color="{COLOR["radical"]}">',
        )
        .replace(
            '<mark title="Kanji" class="kanji-highlight">',
            f'<font color="{COLOR["kanji"]}">',
        )
        .replace(
            '<mark title="Vocabulary" class="vocabulary-highlight">',
            f'<font color="{COLOR["vocabulary"]}">',
        )
        .replace(
            '<mark title="Reading" class="reading-highlight">',
            f'<font color="{COLOR["reading"]}">',
        )
        .replace("</mark>", "</font>")
        .replace("\n", "")
    )
