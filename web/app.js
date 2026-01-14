"use strict";
const summary = document.getElementById("summary");
const greedyButton = document.getElementById("greedyButton");
const ucbButton = document.getElementById("ucbButton");
function renderSummary(data) {
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
function getArms() {
    return document.getElementById("armsInput").value;
}
function getPayload() {
    const rounds = parseInt(document.getElementById("roundsInput").value, 10);
    const epsilon = parseFloat(document.getElementById("epsilonInput").value);
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
