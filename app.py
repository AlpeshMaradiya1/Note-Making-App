from flask import Flask, render_template, request, redirect, url_for
import json
import random
from datetime import datetime

app = Flask(__name__)

# Path to the file where notes will be stored
NOTES_FILE = 'notes.json'

# Function to load notes from the JSON file and ensure each note has an ID
def load_notes():
    try:
        with open(NOTES_FILE, 'r') as file:
            notes = json.load(file)
        # Ensure each note has an ID
        max_id = -1
        for note in notes:
            if 'id' not in note:
                note['id'] = max_id + 1  # Assign a new ID
            max_id = max(max_id, note['id'])
        return notes
    except FileNotFoundError:
        return []

# Function to save notes to the JSON file
def save_notes(notes):
    with open(NOTES_FILE, 'w') as file:
        json.dump(notes, file)

@app.route('/', methods=['GET', 'POST'])
def index():
    notes = load_notes()

    if request.method == 'POST':
        note_content = request.form.get('note')
        if note_content:
            # Assign a random color class to the note
            color_class = f"note-color-{random.randint(1, 5)}"
            # Add timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Assign a unique ID (using the current length of notes as a simple unique identifier)
            note_id = len(notes)
            notes.append({
                'id': note_id,
                'content': note_content,
                'color': color_class,
                'timestamp': timestamp
            })
            save_notes(notes)
        return redirect(url_for('index'))

    return render_template('index.html', notes=notes)

@app.route('/edit/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    notes = load_notes()
    # Find the note with the matching ID
    for note in notes:
        if note['id'] == note_id:
            new_content = request.form.get('new_content')
            if new_content:
                note['content'] = new_content
                note['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Update timestamp
                save_notes(notes)
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    notes = load_notes()
    # Filter out the note with the matching ID
    notes = [note for note in notes if note['id'] != note_id]
    save_notes(notes)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    