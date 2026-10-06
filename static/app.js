const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const inputLabel = document.getElementById("inputLabel");
const submitBtn = document.getElementById("submitBtn");
const clearBtn = document.getElementById("clearBtn");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const statusEl = document.getElementById("status");

const placeholders = {
  qa: ["Your question", "Example: Which is the largest ocean?"],
  explain: ["Topic to explain", "Example: Explain the Pythagoras theorem."],
  quiz: ["Passage or topic", "Paste a passage or enter a topic for a 3-question quiz."],
  summarize: ["Text to summarize", "Paste a paragraph or study material here."],
  learn: ["Topic to learn", "Example: SQL for a beginner who wants to reach an intermediate level."]
};

function updateTaskUI() {
  const [label, placeholder] = placeholders[task.value];
  inputLabel.textContent = label;
  inputText.placeholder = placeholder;
}

task.addEventListener("change", updateTaskUI);
clearBtn.addEventListener("click", () => {
  inputText.value = "";
  result.innerHTML = "";
  resultCard.classList.add("hidden");
  statusEl.textContent = "";
});

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderQuiz(data) {
  return data.questions.map((q, index) => `
    <article class="quiz-question">
      <h3>${index + 1}. ${escapeHtml(q.question)}</h3>
      ${q.options.map((option, optionIndex) => `
        <label class="option">
          <input type="radio" name="q${index}" value="${escapeHtml(option)}">
          ${String.fromCharCode(65 + optionIndex)}. ${escapeHtml(option)}
        </label>
      `).join("")}
      <button type="button" class="secondary" onclick="checkQuizAnswer(${index})">Check answer</button>
      <p id="feedback-${index}"></p>
      <p><strong>Answer:</strong> ${escapeHtml(q.correct_answer)}</p>
      <p>${escapeHtml(q.explanation)}</p>
    </article>
  `).join("");
}

let latestQuiz = null;

window.checkQuizAnswer = function(index) {
  const question = latestQuiz.questions[index];
  const selected = document.querySelector(`input[name="q${index}"]:checked`);
  const feedback = document.getElementById(`feedback-${index}`);

  if (!selected) {
    feedback.textContent = "Choose an option first.";
    return;
  }

  if (selected.value === question.correct_answer) {
    feedback.textContent = "Correct!";
    selected.closest(".option").classList.add("correct");
  } else {
    feedback.textContent = `Not quite. The correct answer is: ${question.correct_answer}`;
    selected.closest(".option").classList.add("wrong");
  }
};

function renderLearningPath(data) {
  return `
    <div class="answer"><strong>${escapeHtml(data.topic)}</strong><br>${escapeHtml(data.overview)}</div>
    ${data.steps.map((step, index) => `
      <article class="step">
        <h3>${index + 1}. ${escapeHtml(step.level)}</h3>
        <p><strong>Estimated time:</strong> ${escapeHtml(step.estimated_time)}</p>
        <p><strong>Topics:</strong> ${step.topics.map(escapeHtml).join(", ")}</p>
        <p><strong>Goals:</strong></p>
        <ul>${step.goals.map(g => `<li>${escapeHtml(g)}</li>`).join("")}</ul>
        <p><strong>Resources:</strong></p>
        ${step.resources.map(r => `
          <div class="resource">
            ${r.url ? `<a href="${escapeHtml(r.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(r.title)}</a>` : `<strong>${escapeHtml(r.title)}</strong>`}
            <div>${escapeHtml(r.type)} — ${escapeHtml(r.description)}</div>
          </div>
        `).join("")}
      </article>
    `).join("")}
  `;
}

async function submit() {
  const text = inputText.value.trim();
  if (!text) {
    alert("Please enter some text first.");
    return;
  }

  const endpoints = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations"
  };

  submitBtn.disabled = true;
  statusEl.textContent = "Generating...";
  resultCard.classList.remove("hidden");
  result.innerHTML = "";

  try {
    const response = await fetch(endpoints[task.value], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "The server returned an error.");
    }

    if (task.value === "quiz") {
      latestQuiz = data;
      result.innerHTML = renderQuiz(data);
    } else if (task.value === "learn") {
      result.innerHTML = renderLearningPath(data);
    } else {
      result.innerHTML = `<div class="answer">${escapeHtml(data.answer || data.result)}</div>`;
    }

    statusEl.textContent = "Done";
  } catch (error) {
    result.innerHTML = `<div class="answer"><strong>Error:</strong> ${escapeHtml(error.message)}</div>`;
    statusEl.textContent = "Failed";
  } finally {
    submitBtn.disabled = false;
  }
}

submitBtn.addEventListener("click", submit);
updateTaskUI();
