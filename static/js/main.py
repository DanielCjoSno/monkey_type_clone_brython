from browser import document, html, ajax, timer, console

INITIAL_TIME = 30

# Variables globales
words = []
currentTime = INITIAL_TIME
playing = False

def init_game():
    try:
        global words, currentTime, playing
        playing = False
        currentTime = INITIAL_TIME

        console.log("Iniciando el juego...")

        # Fetch words from API
        def on_complete(req):
            try:
                global words
                words = req.json
                console.log(f"Palabras recibidas: {words}")
                render_words()
                start_game()
            except Exception as e:
                console.error(f"Error en on_complete: {e}")

        ajax.get('/api/words', oncomplete=on_complete)
    except Exception as e:
        console.error(f"Error en init_game: {e}")

def render_words():
    try:
        paragraph = document['game'].select('p')[0]
        paragraph.clear()
        for word in words:
            word_span = html.SPAN()
            for letter in word:
                letter_span = html.SPAN(letter, Class="letter")
                word_span <= letter_span
            word_span.class_name = "word"
            paragraph <= word_span
        activate_first_word()
    except Exception as e:
        console.error(f"Error en render_words: {e}")

def activate_first_word():
    try:
        first_word = document['game'].select('span.word')[0]
        first_word.class_name += " active"
        first_letter = first_word.select('span.letter')[0]
        first_letter.class_name += " active"
    except Exception as e:
        console.error(f"Error en activate_first_word: {e}")

def start_game():
    try:
        document['input'].value = ""
        document['input'].focus()
        document['time'].text = str(currentTime)
        console.log("Juego iniciado.")
    except Exception as e:
        console.error(f"Error en start_game: {e}")

def on_key_down(event):
    try:
        if not playing:
            start_timer()
        handle_input(event)
    except Exception as e:
        console.error(f"Error en on_key_down: {e}")

def start_timer():
    try:
        global playing
        playing = True
        def countdown():
            try:
                global currentTime
                if currentTime > 0:
                    currentTime -= 1
                    document['time'].text = str(currentTime)
                else:
                    game_over()
            except Exception as e:
                console.error(f"Error en countdown: {e}")

        timer.set_interval(countdown, 1000)
        console.log("Temporizador iniciado.")
    except Exception as e:
        console.error(f"Error en start_timer: {e}")

def handle_input(event):
    try:
        if event.key == " ":
            event.preventDefault()
            move_to_next_word()
        else:
            check_letter(event.key)
            move_to_next_letter()
    except Exception as e:
        console.error(f"Error en handle_input: {e}")

def move_to_next_letter():
    try:
        current_letter = document['game'].select('span.letter.active')[0]
        console.log(f"Moviendo desde la letra: {current_letter.text}")
        current_letter.class_name = current_letter.class_name.replace(" active", "")
        next_letter = current_letter.nextSibling

        # Avanzar hasta encontrar el siguiente hermano que sea una letra
        while next_letter and next_letter.tagName != 'SPAN':
            next_letter = next_letter.nextSibling

        if next_letter and next_letter.tagName == 'SPAN':
            next_letter.class_name += " active"
        else:
            console.log("No se encontró siguiente letra, esperando para mover a la siguiente palabra.")
    except IndexError:
        console.warn("No hay más letras en la palabra.")
    except Exception as e:
        console.error(f"Error en move_to_next_letter: {e}")

def move_to_next_word():
    try:
        current_word = document['game'].select('span.word.active')[0]
        console.log(f"Moviendo desde la palabra: {current_word.text}")
        current_word.class_name = current_word.class_name.replace(" active", "")
        next_word = current_word.nextSibling

        # Avanzar hasta encontrar el siguiente hermano que sea una palabra
        while next_word and next_word.tagName != 'SPAN':
            next_word = next_word.nextSibling

        if next_word and next_word.tagName == 'SPAN':
            next_word.class_name += " active"
            next_letter = next_word.select('span.letter')[0]
            next_letter.class_name += " active"
            document['input'].value = ""
        else:
            game_over()
    except Exception as e:
        console.error(f"Error en move_to_next_word: {e}")

def check_letter(char):
    try:
        current_word = document['game'].select('span.word.active')[0]
        letters = current_word.select('span.letter')
        input_value = document['input'].value + char  # Añadimos el nuevo carácter al valor de entrada

        console.log(f"Valor de entrada: {input_value}")

        for i, letter_span in enumerate(letters):
            if i < len(input_value):
                if input_value[i] == letter_span.text:
                    letter_span.class_name = "letter correct"
                    console.log(f"Letra {letter_span.text} correcta.")
                else:
                    letter_span.class_name = "letter incorrect"
                    console.log(f"Letra {letter_span.text} incorrecta.")
            else:
                letter_span.class_name = "letter"

        if len(input_value) >= len(letters):
            console.log("Palabra completada, esperando espacio para la siguiente palabra.")
    except Exception as e:
        console.error(f"Error en check_letter: {e}")

def game_over():
    try:
        global playing
        playing = False
        # Mostrar resultados
        console.log("Juego terminado.")
    except Exception as e:
        console.error(f"Error en game_over: {e}")

try:
    document['input'].bind('keydown', on_key_down)
    init_game()
except Exception as e:
    console.error(f"Error en la ejecución principal: {e}")
