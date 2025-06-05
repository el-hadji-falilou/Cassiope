// Configuration de Monaco Editor
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.36.1/min/vs' } });

// Initialisation des éditeurs
require(['vs/editor/editor.main'], function () {
    window.monacoEditors = {};

    const editorsConfig = [
        {
            id: 1, height: '700px', code: [
                's = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]',
                'perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]',
                '',
                'global s_inv, perm_inv',
                's_inv = [0]*16',
                'perm_inv = [0]*16',
                '',
                'def init_inverse_ops():',
                '     """This function populates  s_inv et perm_inv to make decryption possible.',
                '     Of course, it should be called BEFORE any decryption operation.',
                '     """',
                '',
                'def encrypt_round(input, key, do_perm):',
                '     """encrypt_round',
                '     Parameters',
                '     ----------',
                '     input   : the input block',
                '     key     : the sub-key for this round',
                '     do_perm : if True, perform the permutation (it is False for the last round)',
                '',
                '     Output',
                '     ------',
                '     the output value for the round',
                '     """',
                '',
                'def encrypt(plaintext, keys):',
                '     """encrypt',
                '     Parameters',
                '     ----------',
                '     plaintext : input plaintext to encrypt',
                '     keys      : array containing the 5 subkeys (i.e. the complete key)',
                '',
                '     Output',
                '     ------',
                '     the encrypted value',
                '     """'
            ].join('\n')
        },
        {
            id: 2, height: '500px', code: [
                'def decrypt_round(input, key, do_perm):',
                '      """decrypt_round',
                '      Parameters',
                '      ----------',
                '      input   : the ciphertext block to decrypt',
                '      key     : round subkey',
                '      do_perm : if True, perform the permutation',
                '',
                '      Output',
                '      ------',
                '      The decrypted plaintext value',
                '      """',
                '',
                'def decrypt(ciphertext, keys):',
                '      """decrypt',
                '      Parameters',
                '      ----------',
                '      ciphertext : ciphertext to decrypt',
                '      keys       : array containing the 5 subkeys (i.e. the complete key)',
                '',
                '      Output',
                '      ------',
                '      The decrypted plaintext',
                '      """'
            ].join('\n')
        },
        {
            id: 4, height: '300px', code: [
                'global probas, s',
                '',
                '# S-Box',
                's = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]',
                '',
                '# Inverse de la S-Box',
                's_inv = [0] * 16',
                '',
                '# probas[i][j] est le nombre de fois qu\'on a δout=j sachant que δin=i',
                'probas = [[0 for _ in range(16)] for _ in range(16)]',
                '',
                '# On calcule le tableau des probas',
                'def compute_probas():',
                ''
            ].join('\n')
        },
        {
            id: 8, height: '500px', code: [
                's = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]',
                'perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]',
                '',
                'global s_inv, perm_inv',
                's_inv = [0]*16',
                'perm_inv = [0]*16',
                '',
                'def init_inverse_ops():',
                '    """This function populates  s_inv et perm_inv to make decryption possible."""',
                '',
                'def perm_inverse(x):',
                '    """',
                '    Applique l\'inverse de la permutation de MiniCipher sur un entier 16 bits.',
                '    """',
                '',
                'def read_cipher_pairs(filename):',
                '    """Reads a text file containing (C, C\') pairs in hexadecimal',
                '    and returns a list of (int, int) tuples."""',
                '',
                'def find_k5_part1() -> int:',
                '    """',
                '    Trouve les 8 bits de k5 (masque 0x0F0F)...',
                '    """',
                '',
                'def find_k5_part2() -> int:',
                '    """',
                '    Trouve les 8 bits de k5 (masque 0xF0F0)...',
                '    """'
            ].join('\n')
        },
        {
            id: 12, height: '300px', code: [
                'def find_k4_part1() -> int:',
                '    """',
                '    Trouve 8 bits de k4 (masque 0x5555)...',
                '    """',
                '',
                'def find_k4_part2() -> int:',
                '    """',
                '    Trouve 8 bits de k4 (masque 0xAAAA)...',
                '    """'
            ].join('\n')
        },
        {
            id: 14, height: '300px', code: [
                'def find_k3_part1() -> int:',
                '    """',
                '    Trouve 8 bits de k3 (masque 0x3333)...',
                '    """',
                '',
                'def find_k3_part2() -> int:',
                '    """',
                '    Trouve 8 bits de k3 (masque 0xCCCC)...',
                '    """'
            ].join('\n')
        },
        {
            id: 15, height: '300px', code: [
                'def find_k2() -> int:',
                '    """',
                '    Trouve k2 complet (16 bits)...',
                '    """',
                '',
                'def find_k1() -> int:',
                '    """',
                '    Trouve k1 (16 bits) après avoir obtenu k2...',
                '    """'
            ].join('\n')
        }
    ];

    editorsConfig.forEach(config => {
        const container = document.getElementById(`editor-container-q${config.id}`);
        if (container) {
            container.style.height = config.height;
            window.monacoEditors[`q${config.id}`] = monaco.editor.create(container, {
                value: config.code,
                language: 'python',
                theme: 'vs-dark',
                automaticLayout: true,
                minimap: { enabled: false },
                fontSize: 14
            });
        }
    });
});

// Fonction de soumission générique pour chaque question (adaptée au backend Flask)
function submitCode(questionId) {
    const idMap = { 1: 'q1', 2: 'q2', 4: 'q4', 8: 'q8', 12: 'q12', 14: 'q14', 15: 'q15' };
    const editorKey = idMap[questionId];
    const editor = window.monacoEditors && window.monacoEditors[editorKey];

    if (!editor) {
        alert("Erreur : éditeur Monaco introuvable pour cette question.");
        return;
    }

    const code = editor.getValue();
    const formData = new FormData();
    const blob = new Blob([code], { type: 'text/plain' });
    formData.append('code', blob, 'code.py');

    let feedbackElem = document.getElementById('feedback-q' + questionId);
    let detailsElem = document.getElementById('details-q' + questionId);

    if (feedbackElem) feedbackElem.textContent = "Correction en cours...";
    if (detailsElem) detailsElem.textContent = "";

    fetch('/submit_code/' + questionId, {
        method: 'POST',
        body: formData
    })
    .then(resp => resp.json())
    .then(data => {
        if (feedbackElem) {
            feedbackElem.textContent = (data.message || data.result || 'Soumission reçue.');
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

function formatOutput(result) {
    let html = `<pre>${result.message || 'Réponse reçue'}`;
    if (result.details) html += `\n\n${result.details}`;
    if (result.stdout) html += `\n\n[Résultat]\n${result.stdout}`;
    if (result.stderr) html += `\n\n[Erreurs]\n${result.stderr}`;
    return html + `</pre>`;
}


async function computeProba() {
    const editor = window.monacoEditors['q4'];
    if (!editor) {
        alert("Erreur : éditeur introuvable pour la question 4.");
        return;
    }

    const code = editor.getValue();
    const blob = new Blob([code], { type: 'text/plain' });
    const formData = new FormData();
    formData.append("code", blob, "question4.py");

    const outputDiv = document.getElementById('output-q4');
    outputDiv.innerHTML = "[Soumission en cours...]";

    try {
        const response = await fetch('/submit_code/4', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.error) {
            outputDiv.innerHTML = `<pre class="error">${result.error}\n${result.details || ''}</pre>`;
        } else {
            let html = `<pre>[Soumission OK]\n${result.message || ''}`;
            if (result.details) html += `\n\n${result.details}`;
            if (result.stdout) html += `\n\n[Résultat]\n${result.stdout}`;
            if (result.stderr) html += `\n\n[Erreur]\n${result.stderr}`;
            html += `</pre>`;
            outputDiv.innerHTML = html;

            await fillProbabilityTable();
        }
    } catch (error) {
        outputDiv.innerHTML = `<pre class="error">Erreur réseau ou serveur : ${error}</pre>`;
    }
}

async function fillProbabilityTable() {
    const response = await fetch('/get_probas');
    const data = await response.json();

    const rows = document.querySelectorAll("#table_1 tr");

    for (let i = 2; i < rows.length; i++) {
        const cells = rows[i].querySelectorAll("td");
        const delta_in = i - 2;
        for (let j = 0; j < 16; j++) {
            cells[j].textContent = data[delta_in][j];
        }
    }
}

function validateInput(questionId, side = "default") {
  let data = {};
  
  // Gestion spécifique pour chaque question
  if (questionId === 5) {
      // Logique existante pour la Q5 (tableau)
      const inputs = document.querySelectorAll(`#table_2 input`);
      data.deltaOut = {};
      data.proba = {};
      
      inputs.forEach((input, index) => {
          if (index < 16) {
              data.deltaOut[`val${index}`] = input.value.trim().toUpperCase();
          } else {
              data.proba[`val${index-16}`] = input.value.trim();
          }
      });
  } 
  else if ([6, 7, 10, 11].includes(questionId)) {
      const table = document.getElementById(`question-${questionId}-table`);
      const proba = document.getElementById(`question-${questionId}-proba`);
      const inputsTable = table ? Array.from(table.querySelectorAll('input')) : [];
      const inputsProba = proba ? Array.from(proba.querySelectorAll('input')) : [];
      const allInputs = [...inputsTable, ...inputsProba];

      allInputs.forEach((input, index) => {
          data[`val${index}`] = input.value.trim().toUpperCase();
      });
  }
  else if (questionId === 13) {
    const table = document.getElementById(`question-${questionId}-${side}-table`);
    const proba = document.getElementById(`question-${questionId}-${side}-proba`);
    const inputsTable = table ? Array.from(table.querySelectorAll('input')) : [];
    const inputsProba = proba ? Array.from(proba.querySelectorAll('input')) : [];
    const allInputs = [...inputsTable, ...inputsProba];

    allInputs.forEach((input, index) => {
        data[`val${index}`] = input.value.trim().toUpperCase();
    });
  }

  const resultDiv = document.getElementById(`result-${questionId}${side !== 'default' ? '-' + side : ''}`);
  resultDiv.innerHTML = '<i>Validation en cours...</i>';

  fetch(`/validate_input/${questionId}/${side}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
  })
  .then(response => {
      if (!response.ok) throw new Error('Erreur réseau');
      return response.json();
  })
  .then(result => {
      resultDiv.innerHTML = result.message;
      resultDiv.className = result.result === "success" ? "success-message" : "error-message";
  })
  .catch(error => {
      resultDiv.innerHTML = `Erreur: ${error.message}`;
      resultDiv.className = "error-message";
  });
}
