def convert_to_gift(questions):
    """
    Convert the generated questions to GIFT format.

    Args:
        questions (list): The list of generated questions.

    Returns:
        str: The questions in GIFT format.
    """
    gift_format = ""
    for q in questions:
        gift_format += str(q) + "\n\n"
    return gift_format
