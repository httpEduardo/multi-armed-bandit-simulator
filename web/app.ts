const summary = document.getElementById("summary") as HTMLDivElement;
const greedyButton = document.getElementById("greedyButton") as HTMLButtonElement;
const ucbButton = document.getElementById("ucbButton") as HTMLButtonElement;

function renderSummary(data: { counts: number[]; averages: number[]; total_reward: number }): void {
  summary.innerHTML = "";
  const items = [
    `Total reward: ${data.total_reward}`,
    `Counts: ${data.counts.join(", ")}`,
    `Avg reward: ${data.averages.join(", ")}`,
  ];
  items.forEach((text) => {
    const card = document.createElement("div");
    card.className = "summary-card";
    card.textContent = text;
    summary.appendChild(card);
  });
}

function getArms(): string {
  return (document.getElementById("armsInput") as HTMLInputElement).value;
}

function getPayload(): { arms: string; rounds: number; epsilon?: number } {
  const rounds = parseInt((document.getElementById("roundsInput") as HTMLInputElement).value, 10);
  const epsilon = parseFloat((document.getElementById("epsilonInput") as HTMLInputElement).value);
  return { arms: getArms(), rounds, epsilon };
}

greedyButton.addEventListener("click", () => {
  fetch("/api/simulate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(getPayload()),
  })
    .then((res) => res.json())
    .then((data) => renderSummary(data));
});

ucbButton.addEventListener("click", () => {
  const payload = getPayload();
  fetch("/api/ucb", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ arms: payload.arms, rounds: payload.rounds }),
  })
    .then((res) => res.json())
    .then((data) => renderSummary(data));
});
