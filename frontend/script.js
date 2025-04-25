
document.getElementById('nameForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const data = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        birth_date: document.getElementById('birthDate').value,
        gender: document.getElementById('gender').value,
        nationality: document.getElementById('nationality').value
    };
    const response = await fetch('http://localhost:5000/api/generate-name', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await response.json();
    document.getElementById('resultArea').innerHTML = `<h2>生成名字：${result.chinese_name}</h2><p>${result.explanation}</p>`;
});
