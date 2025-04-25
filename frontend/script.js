// 初始化配置
const API_ENDPOINT = '/api/generate-name';
const LOADER_DELAY = 300; // 防止加载闪烁

// DOM元素引用
const dom = {
  form: document.getElementById('nameForm'),
  resultSection: document.getElementById('resultSection'),
  nameCards: document.getElementById('nameCards'),
  modal: document.getElementById('detailModal'),
  loader: document.querySelector('.loader'),
  btnText: document.querySelector('.btn-text')
};

// 表单提交处理
dom.form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = {
    first_name: dom.form.querySelector('#firstName').value.trim(),
    last_name: dom.form.querySelector('#lastName').value.trim(),
    birthdate: dom.form.querySelector('#dob').value,
    nationality: dom.form.querySelector('#nationality').value,
    gender: 'unknown' // 可根据需要添加性别选择
  };

  if (validateForm(formData)) {
    toggleLoader(true);
    
    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      
      renderResults(data.results);
      triggerConfetti();
      
    } catch (error) {
      showError('无法生成名字，请稍后重试');
    } finally {
      toggleLoader(false);
    }
  }
});

// 表单验证
function validateForm({ first_name, last_name, birthdate, nationality }) {
  if (!first_name || !last_name) {
    showError('请填写完整姓名');
    return false;
  }
  
  if (!/^\d{4}-\d{2}-\d{2}$/.test(birthdate)) {
    showError('请选择有效出生日期');
    return false;
  }
  
  return true;
}

// 渲染结果卡片
function renderResults(results) {
  dom.nameCards.innerHTML = results.map((result, index) => `
    <div class="name-card" data-index="${index}">
      <h3>${result.name}</h3>
      <div class="meta-info">
        <span class="score">✦ 评分 ${result.score.toFixed(1)}</span>
        <button class="detail-btn">文化解析 →</button>
      </div>
    </div>
  `).join('');

  dom.resultSection.classList.remove('hidden');
  initCardEvents();
}

// 初始化卡片事件
function initCardEvents() {
  dom.nameCards.addEventListener('click', (e) => {
    const card = e.target.closest('.name-card');
    const btn = e.target.closest('.detail-btn');
    
    if (card && btn) {
      const index = card.dataset.index;
      showDetailModal(currentResults[index]);
    }
  });
}

// 显示详情模态框
function showDetailModal(data) {
  const { name, cultural_insights, poetry_references } = data;
  
  dom.modal.querySelector('#modalName').textContent = name;
  dom.modal.querySelector('#culturalMeaning').textContent = 
    cultural_insights.name_origin === 'classic_poetry' 
      ? '源自经典诗词，蕴含深厚文化底蕴' 
      : '音译优化，兼顾发音美感与文化内涵';
  
  dom.modal.querySelector('#poetryReference').innerHTML = poetry_references
    .map(ref => `<p>${ref}</p>`)
    .join('') || '<em>此名字为创新组合</em>';
  
  dom.modal.classList.remove('hidden');
}

// 通用功能
function toggleLoader(show) {
  document.querySelector('.generate-btn').disabled = show
  document.getElementById('loader').style.display = show ? 'block' : 'none'
  document.querySelector('.btn-text').style.opacity = show ? 0.5 : 1
}

function showError(message) {
  const alertEl = document.createElement('div');
  alertEl.className = 'error-alert';
  alertEl.textContent = message;
  document.body.appendChild(alertEl);
  
  setTimeout(() => alertEl.remove(), 3000);
}

function triggerConfetti() {
  const canvas = document.getElementById('confettiCanvas');
  canvas.classList.remove('hidden');
  
  // 可在此集成第三方confetti库
  setTimeout(() => canvas.classList.add('hidden'), 2000);
}

// 模态框控制
document.querySelector('.close-btn').addEventListener('click', () => {
  dom.modal.classList.add('hidden');
});

document.getElementById('retryBtn').addEventListener('click', () => {
  dom.form.dispatchEvent(new Event('submit'));
  dom.modal.classList.add('hidden');
});

// 分享功能
document.getElementById('downloadBtn').addEventListener('click', () => {
  const name = dom.modal.querySelector('#modalName').textContent;
  alert(`已生成 ${name} 的艺术卡片，可右键保存`);
});
