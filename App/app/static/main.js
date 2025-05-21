// Placez ici votre code AJAX si nécessaire
console.log("static/main.js loaded");
// main.js

let editor;

require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' }});

require(['vs/editor/editor.main'], function() {
    editor = monaco.editor.create(document.getElementById('monaco-container'), {
        value: [
            '# Implémentez ici vos fonctions MiniCipher',
            'def encrypt_block(plaintext, key):',
            '    pass',
        ].join('\n'),
        language: 'python',
        theme: 'vs-light',
        fontSize: 16,
        automaticLayout: true
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const submitBtn = document.getElementById('submit-code-btn');
    const feedbackZone = document.getElementById('submission-feedback');

    submitBtn.onclick = function() {
        const code = editor.getValue();
        feedbackZone.textContent = "Envoi du code...";
        fetch('/tp/submit_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        })
        .then(resp => resp.json())
        .then(data => {
            feedbackZone.textContent = data.message || 'Soumission reçue.';
            if (data.success === false) {
                feedbackZone.style.color = 'red';
            } else {
                feedbackZone.style.color = 'green';
            }
        })
        .catch(err => {
            feedbackZone.textContent = "Erreur d'envoi : " + err;
            feedbackZone.style.color = 'red';
        });
    }
});
