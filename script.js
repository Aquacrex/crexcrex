let currentAnswer = {};

async function loadQuestion() {
    const response = await fetch("http://localhost:8000/quiz?taxon=Fungi");
    const data = await response.json();
    document.getElementById("quiz-image").src = data.image;
    currentAnswer = data.answer;
}

function checkAnswer() {
    const userGuess = document.getElementById("guess").value.toLowerCase();
    const actualSpecies = currentAnswer.species.toLowerCase();
    const resultEl = document.getElementById("result");
    
    if (userGuess === actualSpecies) {
        resultEl.textContent = "Correct";
    } else {
        resultEl.textContent = `Wrong, it's a ${currentAnswer.species}.`;
    }
}

// Load first question on startup
loadQuestion();