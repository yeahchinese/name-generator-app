// Handle form submit
document.getElementById("nameForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const first = document.getElementById("firstName").value.trim();
  const last = document.getElementById("lastName").value.trim();
  const dob = document.getElementById("dob").value;
  const nation = document.getElementById("nationality").value;

  if (!first || !last || !dob || !nation) return;

  // Fake generation (to be replaced by backend)
  const fullName = "叶可可"; // Replace with real logic later
  const poem = "山有木兮木有枝，心悦君兮君不知";
  const meaning = "温润如玉，才华横溢";

  document.getElementById("chineseName").textContent = fullName;
  document.getElementById("meaningText").textContent = meaning;
  document.getElementById("poemText").textContent = poem;
  document.getElementById("lunarDateText").textContent = "农历乙巳年七月初七"; // 示例

  document.getElementById("resultArea").classList.remove("hidden");

  // Trigger confetti
  const confetti = document.getElementById("confettiContainer");
  confetti.classList.remove("hidden");
  setTimeout(() => confetti.classList.add("hidden"), 3000);
});

// Show modal
document.getElementById("detailBtn").addEventListener("click", () => {
  document.getElementById("detailModal").classList.remove("hidden");
});

// Hide modal
document.getElementById("closeModal").addEventListener("click", () => {
  document.getElementById("detailModal").classList.add("hidden");
});

// Retry button
document.getElementById("retryBtn").addEventListener("click", () => {
  document.getElementById("nameForm").reset();
  document.getElementById("resultArea").classList.add("hidden");
  document.getElementById("detailModal").classList.add("hidden");
});

// Share (placeholder)
document.getElementById("shareBtn").addEventListener("click", () => {
  alert("分享功能需集成真实社交媒体 API（如微信/微博/推特）");
});
