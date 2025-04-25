// frontend/script.js
const API_ENDPOINT = '/api/generate-name';
const dom = {
    form: document.getElementById('nameForm'),
    results: document.getElementById('results'),
    nameCards: document.getElementById('nameCards'),
    modal: document.getElementById('modal'),
    loader: document.querySelector('.loader'),
    btnText: document.querySelector('.btn-text')
};

// 表单提交处理
dom.form.addEventListener('submit', async (e) => {
    e.preventDefault();
    toggleLoader(true);

    const formData = {
        first_name: dom.form.querySelector('#firstName').value.trim(),
        last_name: dom.form.querySelector('#lastName').value.trim(),
        birthdate: dom.form.querySelector('#dob').value,
        nationality: dom.form.querySelector('#nationality').value
    };

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Generation failed');
        const data = await response.json();
        
        renderResults(data.results);
        dom.results.classList.remove('hidden');
        
    } catch (error) {
        showError('无法生成名字，请稍后重试');
    } finally {
        toggleLoader(false);
    }
});

// 渲染结果
function renderResults(results) {
    dom.nameCards.innerHTML = results.map((result, index) => `
        <div class="name-card" data-index="${index}">
            <h3>${result.name}</h3>
            <div class="meta">
                <span class="pinyin">${result.pinyin}</span>
                <button class="detail-btn">文化解析 →</button>
            </div>
        </div>
    `).join('');

    // 绑定详情点击事件
    document.querySelectorAll('.detail-btn').forEach(btn => {
        btn.addEventListener('click', showDetail);
    });
}

// 显示详情模态
function showDetail(e) {
    const card = e.target.closest('.name-card');
    const index = card.dataset.index;
    const result = currentResults[index];
    
    document.getElementById('modalName').textContent = result.name;
    document.getElementById('culturalMeaning').textContent = result.cultural_insights.meaning;
    document.getElementById('poetryReference').textContent = result.poetry[0] || '此名为创新组合';
    
    dom.modal.classList.remove('hidden');
}

// 通用功能
function toggleLoader(show) {
    dom.loader.style.display = show ? 'block' : 'none';
    dom.btnText.style.opacity = show ? 0.5 : 1;
    dom.form.querySelector('button').disabled = show;
}

function showError(message) {
    const alert = document.createElement('div');
    alert.className = 'error-alert';
    alert.textContent = message;
    document.body.appendChild(alert);
    
    setTimeout(() => alert.remove(), 3000);
}

// 模态控制
document.querySelector('.close-btn').addEventListener('click', () => {
    dom.modal.classList.add('hidden');
});

document.getElementById('retryBtn').addEventListener('click', () => {
    dom.form.dispatchEvent(new Event('submit'));
    dom.modal.classList.add('hidden');
});

// 初始化
let currentResults = [];
