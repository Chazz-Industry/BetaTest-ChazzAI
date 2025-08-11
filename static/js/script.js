const tabWrite = document.getElementById('tab-write');
const tabTalk = document.getElementById('tab-talk');
const formWrite = document.getElementById('form-write');
const formTalk = document.getElementById('form-talk');

tabWrite.addEventListener('click', () => {
    tabWrite.classList.add('active');
    tabTalk.classList.remove('active');
    formWrite.classList.add('active');
    formTalk.classList.remove('active');
});

tabTalk.addEventListener('click', () => {
    tabTalk.classList.add('active');
    tabWrite.classList.remove('active');
    formTalk.classList.add('active');
    formWrite.classList.remove('active');
});

/***********************************************************************************************************
 *                                             CLIPBOARD FUNCTION                                          *
 ***********************************************************************************************************/

function copyResult(btn) {
  const resultText = document.getElementById("result-text");
  if (!resultText) return;

  const text = resultText.innerText;

  navigator.clipboard.writeText(text).then(() => {
    const btnText = btn.querySelector(".btn-text");
    btn.classList.add("copied");
    btnText.textContent = "Copié !";

    setTimeout(() => {
      btn.classList.remove("copied");
      btnText.textContent = "Copier";
    }, 2000);
  }).catch(() => {
    const btnText = btn.querySelector(".btn-text");
    btn.classList.add("copied");
    btnText.textContent = "Erreur";

    setTimeout(() => {
      btn.classList.remove("copied");
      btnText.textContent = "Copier";
    }, 2000);
  });
}

async function send() {
  const msg = document.getElementById("message").value.trim();
  const context = document.getElementById("context").value.trim();
  const mode = document.getElementById("mode").value;
  const resultBox = document.getElementById("result");
  const resultText = document.getElementById("result-text");

  resultBox.classList.remove("visible");
  resultText.innerText = "";

  if (!msg && mode === "rewrite") {
    alert("Merci d'entrer un message à réécrire.");
    return;
  }

  let url;
  switch (mode) {
    case "rewrite":
      url = "/rewrite";
      break;
    case "generate":
      url = "/generate";
      break;
    default:
      alert("Mode inconnu !");
      return;
  }

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, context: context, mode: mode })
    });

    const data = await res.json();

    if (data && data.suggestion) {
      resultText.innerText = data.suggestion.replace(/"/g, '');
      resultBox.classList.add("visible");
    } else {
      resultText.innerText = "Aucune suggestion générée.";
      resultBox.classList.add("visible");
    }

  } catch (error) {
    console.error("Erreur lors de l'envoi :", error);
    resultText.innerText = "❌ Une erreur s'est produite.";
    resultBox.classList.add("visible");
  }
}
