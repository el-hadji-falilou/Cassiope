// Charger Monaco Editor pour plusieurs questions
require.config({ paths: { 'vs': 'https://unpkg.com/monaco-editor/min/vs' } });

require(['vs/editor/editor.main'], function () {
    window.monacoEditors = {};

    [
        { id: 'q1', question: 1, code: "# Implémentez encrypt_round & encrypt\n" },
        { id: 'q2', question: 2, code: "# Implémentez decrypt & decrypt_round\n" },
        { id: 'q4', question: 4, code: "# Implémentez compute_probas\n" },
        { id: 'q8', question: 8, code: "# Implémentez attaque diff K5\n" },
        { id: 'q12', question: 12, code: "# Code pour k4\n" },
        { id: 'q14', question: 14, code: "# Code pour k3\n" },
        { id: 'q15', question: 15, code: "# Code pour k2/k1\n" }
    ].forEach(function (info) {
        var container = document.getElementById('editor-container-' + info.id);
        if (container) {
            window.monacoEditors[info.id] = monaco.editor.create(container, {
                value: info.code,
                language: 'python',
                theme: 'vs-dark',
                fontSize: 15,
                automaticLayout: true
            });
        }
    });
});

// Fonction de soumission générique pour chaque question (adaptée au backend Flask)
function submitCode(questionId) {
    // Associer ID <-> nom de l'éditeur
    const idMap = { 1: 'q1', 2: 'q2', 4: 'q4', 8: 'q8', 12: 'q12', 14: 'q14', 15: 'q15' };
    const editorKey = idMap[questionId];
    const editor = window.monacoEditors && window.monacoEditors[editorKey];

    if (!editor) {
        alert("Erreur : éditeur Monaco introuvable pour cette question.");
        return;
    }

    // Récupérer le code de l’éditeur
    const code = editor.getValue();

    // Créer un objet FormData pour uploader le code comme fichier (clé 'code')
    const formData = new FormData();
    const blob = new Blob([code], { type: 'text/plain' });
    formData.append('code', blob, 'code.py');

    // Sélecteurs pour le feedback principal et le détail
    let feedbackElem = document.getElementById('feedback-q' + questionId);
    let detailsElem = document.getElementById('details-q' + questionId);

    if (feedbackElem) feedbackElem.textContent = "Correction en cours...";
    if (detailsElem) detailsElem.textContent = ""; // reset

    // Envoi au backend : /submit_code/<id>
    fetch('/submit_code/' + questionId, {
        method: 'POST',
        body: formData
    })
    .then(resp => resp.json())
    .then(data => {
        if (feedbackElem) {
            feedbackElem.textContent = (data.message || data.result || 'Soumission reçue.');
            detailsElem.textContent = data.details || "";
            feedbackElem.className = data.status === 'SUCCESS' ? 'success-message' : 'error-message';
        }
        if (detailsElem) {
            detailsElem.textContent = data.details || "";
        }
    })
    .catch(err => {
        if (feedbackElem) {
            feedbackElem.textContent = "Erreur d'envoi : " + err;
            feedbackElem.className = 'error-message';
        }
        if (detailsElem) {
            detailsElem.textContent = "";
        }
    });
}

// Attacher le handler à chaque bouton de question au chargement
document.addEventListener("DOMContentLoaded", function() {
    [
        { id: 'q1', question: 1 },
        { id: 'q2', question: 2 },
        { id: 'q4', question: 4 },
        { id: 'q8', question: 8 },
        { id: 'q12', question: 12 },
        { id: 'q14', question: 14 },
        { id: 'q15', question: 15 }
    ].forEach(function (info) {
        var btn = document.getElementById('submit-' + info.id);
        if (btn) btn.onclick = function() { submitCode(info.question); };
    });
});
