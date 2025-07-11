/*let currentQuestionIndex = 0;
let questions = [];
let selectedOption = null;
let userAnswers = [];

async function fetchQuestions() {
  try {
    const response = await fetch('/get-tech-questions');
    questions = await response.json();
    renderBubbles();
    displayQuestion();
  } catch (err) {
    document.getElementById('quiz-container').innerHTML = "<p>Failed to load questions.</p>";
    console.error('Error fetching technical questions:', err);
  }
}

function renderBubbles() {
  const tracker = document.getElementById('bubble-tracker');
  tracker.innerHTML = '';
  questions.forEach((_, index) => {
    const bubble = document.createElement('span');
    bubble.className = 'bubble';
    bubble.innerText = index + 1;
    tracker.appendChild(bubble);
  });
}

function highlightBubble(index) {
  const bubbles = document.querySelectorAll('.bubble');
  bubbles.forEach((b, i) => {
    b.classList.toggle('active', i === index);
  });
}

function displayQuestion() {
  if (currentQuestionIndex >= questions.length) {
    document.getElementById('quiz-container').style.display = "none";
    document.getElementById('completionMessage').style.display = "block";

   const messageBox = document.getElementById('completionMessage');
if (!document.querySelector('.loading-msg')) {
  const loading = document.createElement('p');
  loading.className = 'loading-msg';
  loading.innerText = "Submitting your answers...";
  messageBox.appendChild(loading);
}


    submitTechnicalAnswers(); // Now handles redirection
    return;
  }

  highlightBubble(currentQuestionIndex);
  selectedOption = null;

  const q = questions[currentQuestionIndex];
  document.getElementById('question-number').innerText = `Question ${currentQuestionIndex + 1}`;
  document.getElementById('question-text').innerText = q.Question;
  document.getElementById('option-A').innerText = q["Option A"];
  document.getElementById('option-B').innerText = q["Option B"];
  document.getElementById('option-C').innerText = q["Option C"];
  document.getElementById('option-D').innerText = q["Option D"];

  const buttons = document.querySelectorAll('.option-btn');
  buttons.forEach(button => {
    button.disabled = false;
    button.style.backgroundColor = '#7873f5';
    button.onclick = () => {
      selectedOption = button;
      buttons.forEach(btn => btn.style.backgroundColor = '#7873f5');
      button.style.backgroundColor = '#3e5ee0';
    };
  });

  let nextBtn = document.querySelector('.continue-btn');
  if (!nextBtn) {
    nextBtn = document.createElement('button');
    nextBtn.className = 'continue-btn option-btn';
    nextBtn.innerText = 'Next';
    document.getElementById('quiz-container').appendChild(nextBtn);
  }

  nextBtn.onclick = () => {
    const selectedText = selectedOption ? selectedOption.innerText.trim() : "";
    userAnswers.push(selectedText);
    setTimeout(() => {
      currentQuestionIndex++;
      displayQuestion();
    }, 500);
  };
}


function submitTechnicalAnswers() {
  const urlParams = new URLSearchParams(window.location.search);
  const aptitude = urlParams.get('aptitude') || 0;
  const communication = urlParams.get('communication') || 0;

  fetch(`/submit-tech-answers?aptitude=${aptitude}&communication=${communication}`, {
    method: 'POST',
    body: JSON.stringify({ userAnswers }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (!response.ok) throw new Error('Failed network request');
    return response.json();
  })
  .then(data => {
    window.location.href = data.redirect;
  })
  .catch(err => {
    console.error('Error submitting technical answers:', err);
    document.getElementById('completionMessage').innerText = "Failed to submit answers.";
  });
}


function submitComAssessment() {
  // Calculate score...
  const percentage = (score / questions.length) * 100;

  // Redirect to Communication Assessment with score
window.location.href = `/form?aptitude_score=${aptitudeScore}&communication_score=${commScore}&technical_score=${techScore}`;
}
window.onload = fetchQuestions;

*/
let currentQuestionIndex = 0; 
let questions = [];
let selectedOption = null;
let userAnswers = [];

async function fetchQuestions() {
  try {
    const response = await fetch('/get-tech-questions');
    questions = await response.json();
    renderBubbles();
    displayQuestion();
  } catch (err) {
    document.getElementById('quiz-container').innerHTML = "<p>Failed to load questions.</p>";
    console.error('Error fetching technical questions:', err);
  }
}

function renderBubbles() {
  const tracker = document.getElementById('bubble-tracker');
  tracker.innerHTML = '';
  questions.forEach((_, index) => {
    const bubble = document.createElement('span');
    bubble.className = 'bubble';
    bubble.innerText = index + 1;
     bubble.addEventListener('click', () => {
  currentQuestionIndex = index;
  displayQuestion();
    
  });
tracker.appendChild(bubble);
 
});

}

function highlightBubble(index) {
  const bubbles = document.querySelectorAll('.bubble');
  bubbles.forEach((b, i) => {
    b.classList.toggle('active', i === index);
  });
}

function displayQuestion() {
  if (currentQuestionIndex >= questions.length) {
    document.getElementById('quiz-container').style.display = "none";
    document.getElementById('completionMessage').style.display = "block";

    const messageBox = document.getElementById('completionMessage');
    if (!document.querySelector('.loading-msg')) {
      const loading = document.createElement('p');
      loading.className = 'loading-msg';
      loading.innerText = "Submitting your answers...";
      messageBox.appendChild(loading);
    }

    submitTechnicalAnswers(); // Handles redirection
    return;
  }

  highlightBubble(currentQuestionIndex);
  selectedOption = null;

  const q = questions[currentQuestionIndex];
  document.getElementById('question-number').innerText = `Question ${currentQuestionIndex + 1}`;
  document.getElementById('question-text').innerText = q.Question;
  document.getElementById('option-A').innerText = q["Option A"];
  document.getElementById('option-B').innerText = q["Option B"];
  document.getElementById('option-C').innerText = q["Option C"];
  document.getElementById('option-D').innerText = q["Option D"];

  const buttons = document.querySelectorAll('.option-btn');
  buttons.forEach(button => {
    button.disabled = false;
    button.style.backgroundColor = '#7873f5';
  });

  const A = document.getElementById('option-A');
  A.onclick = () => {
    selectedOption = 'A';
    buttons.forEach(btn => btn.style.backgroundColor = '#7873f5');
    A.style.backgroundColor = '#3e5ee0';
  }
  const B = document.getElementById('option-B');
  B.onclick = () => {
    selectedOption = 'B';
    buttons.forEach(btn => btn.style.backgroundColor = '#7873f5');
    B.style.backgroundColor = '#3e5ee0';
  }
  const C = document.getElementById('option-C');
  C.onclick = () => {
    selectedOption = 'C';
    buttons.forEach(btn => btn.style.backgroundColor = '#7873f5');
    C.style.backgroundColor = '#3e5ee0';
  }
  const D = document.getElementById('option-D');
  D.onclick = () => {
    selectedOption = 'D';
    buttons.forEach(btn => btn.style.backgroundColor = '#7873f5');
    D.style.backgroundColor = '#3e5ee0';
  }


  let nextBtn = document.querySelector('.continue-btn');
  if (!nextBtn) {
    nextBtn = document.createElement('button');
    nextBtn.className = 'continue-btn option-btn';
    nextBtn.innerText = 'Next';
    document.getElementById('quiz-container').appendChild(nextBtn);
  }

  nextBtn.onclick = () => {
    const selectedText = selectedOption ? selectedOption : "";
    userAnswers.push(selectedText);
    setTimeout(() => {
      currentQuestionIndex++;
      displayQuestion();
    }, 500);
  };
}

function submitTechnicalAnswers() {
  const urlParams = new URLSearchParams(window.location.search);
  const aptitude = urlParams.get('aptitude') || 0;
  const communication = urlParams.get('communication') || 0;
  console.log(communication , aptitude);
  fetch(`/submit-tech-answers?aptitude=${aptitude}&communication=${communication}`, {
    method: 'POST',
    body: JSON.stringify({ userAnswers }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (!response.ok) throw new Error('Failed network request');
    return response.json();
  })
  .then(data => {
    window.location.href = data.redirect;
  })
  .catch(err => {
    console.error('Error submitting technical answers:', err);
    document.getElementById('completionMessage').innerText = "Failed to submit answers.";
  });
}

window.onload = fetchQuestions;
