let currentQuestionIndex = 0;
let questions = [];
let userAnswers = [];
let selectedOption = "";

async function fetchQuestions() {
  try {
    const response = await fetch('/get-questions');
    questions = await response.json();
    renderBubbles();
    displayQuestion();
  } catch (err) {
    document.getElementById('quiz-container').innerHTML = "<p>Failed to load questions.</p>";
    console.error('Error fetching aptitude questions:', err);
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
      selectedOption = userAnswers[index] || "";
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
  const container = document.getElementById('quiz-container');

  if (currentQuestionIndex >= questions.length) {
    container.innerHTML = `
      <h2>✅ You’ve completed the Aptitude Assessment!</h2>
      <button class="com" onclick="submitAptitude()">Continue to Communication Assessment</button>
    `;
    return;
  }

  const q = questions[currentQuestionIndex];

  container.innerHTML = `
    <h2>Question ${currentQuestionIndex + 1}</h2>
    <p class="question">${q.Question}</p>
    <div class="options">
      <button class="option-btn" id="option-A" onclick="selectAnswer('A')">${q["Option A"]}</button>
      <button class="option-btn" id="option-B" onclick="selectAnswer('B')">${q["Option B"]}</button>
      <button class="option-btn" id="option-C" onclick="selectAnswer('C')">${q["Option C"]}</button>
      <button class="option-btn" id="option-D" onclick="selectAnswer('D')">${q["Option D"]}</button>
    </div>
    <button class="com" onclick="nextQuestion()">Next</button>
  `;

  if (selectedOption) {
    const selectedBtn = document.getElementById(`option-${selectedOption}`);
    if (selectedBtn) selectedBtn.classList.add("selected-option");
  }

  highlightBubble(currentQuestionIndex);
}

function selectAnswer(opt) {
  selectedOption = opt;

  document.querySelectorAll('.option-btn').forEach(btn => {
    btn.classList.remove("selected-option");
  });

  const selectedBtn = document.getElementById(`option-${opt}`);
  if (selectedBtn) selectedBtn.classList.add("selected-option");
}

function nextQuestion() {
  if (!selectedOption) {
    alert("Please select an option before continuing.");
    return;
  }

  userAnswers[currentQuestionIndex] = selectedOption;
  selectedOption = "";
  currentQuestionIndex++;
  displayQuestion();
}

function submitAptitude() {
  fetch('/submit-aptitude-answers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userAnswers })
  })
    .then(res => res.json())
    .then(data => {
      if (data.redirect) {
        window.location.href = data.redirect;
      }
    });
}
let score = 0;

function submitAptitudeAssessment() {
  // Calculate score...
  const percentage = (score / questions.length) * 100;
  alert(percentage);
  console.log(percentage);
  // Redirect to Communication Assessment with score
  window.location.href = `/Comassessment?aptitude=${percentage.toFixed(2)}`;
}


window.onload = fetchQuestions;
