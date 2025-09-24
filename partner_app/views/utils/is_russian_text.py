def is_valid_russian_text(text: str) -> bool:
    for char in text:
        if not (('а' <= char <= 'я') or ('А' <= char <= 'Я') or char in 'ёЁ' or char == '-'):
            return False
    return True