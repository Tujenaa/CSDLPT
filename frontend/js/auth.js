/* ─────────────────────────────────
   AUTH.JS — Đăng nhập & Đăng ký
───────────────────────────────── */

/* ── TOAST ── */
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 2800);
}

/* ── TOGGLE PASSWORD VISIBILITY ── */
function togglePass(inputId, btn) {
  const input = document.getElementById(inputId);
  const icon  = document.getElementById('eyeIcon-' + inputId);
  const isHidden = input.type === 'password';
  input.type = isHidden ? 'text' : 'password';
  icon.innerHTML = isHidden
    ? `<path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/>
       <path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/>
       <line x1="1" y1="1" x2="23" y2="23"/>`
    : `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
       <circle cx="12" cy="12" r="3"/>`;
}

/* ── PASSWORD STRENGTH ── */
function checkStrength(val) {
  const wrap  = document.getElementById('strengthWrap');
  const fill  = document.getElementById('strengthFill');
  const label = document.getElementById('strengthLabel');
  if (!val) { wrap.style.display = 'none'; return; }
  wrap.style.display = 'block';

  let score = 0;
  if (val.length >= 8)  score++;
  if (/[A-Z]/.test(val)) score++;
  if (/[0-9]/.test(val)) score++;
  if (/[^A-Za-z0-9]/.test(val)) score++;

  const levels = [
    { w: '25%', bg: '#ef4444', text: 'Rất yếu' },
    { w: '50%', bg: '#f97316', text: 'Yếu' },
    { w: '75%', bg: '#eab308', text: 'Trung bình' },
    { w: '100%', bg: '#22c55e', text: 'Mạnh' },
  ];
  const lvl = levels[score - 1] || levels[0];
  fill.style.width      = lvl.w;
  fill.style.background = lvl.bg;
  label.textContent     = lvl.text;
  label.style.color     = lvl.bg;
}

/* ── SHOW / HIDE FIELD ERROR ── */
function showError(id, show) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle('show', show);
}
function setInputError(inputId, hasError) {
  const el = document.getElementById(inputId);
  if (!el) return;
  el.classList.toggle('error', hasError);
}

/* ── LOGIN ── */
function handleLogin(e) {
  e.preventDefault();
  const phone = document.getElementById('loginPhone').value.trim();
  const pass  = document.getElementById('loginPass').value;

  let valid = true;

  if (!phone) {
    showError('phoneError', true);
    setInputError('loginPhone', true);
    valid = false;
  } else {
    showError('phoneError', false);
    setInputError('loginPhone', false);
  }

  if (!pass) {
    showError('passError', true);
    setInputError('loginPass', true);
    valid = false;
  } else {
    showError('passError', false);
    setInputError('loginPass', false);
  }

  if (!valid) return;

  const btn = document.getElementById('loginBtn');
  btn.textContent = 'Đang đăng nhập...';
  btn.disabled = true;

  // Simulate API call
  setTimeout(() => {
    btn.textContent = 'Đăng nhập';
    btn.disabled = false;
    showToast('Đăng nhập thành công! Đang chuyển hướng...');
    setTimeout(() => { window.location = '/frontend/history.html'; }, 1200);
  }, 1200);
}

/* ── REGISTER ── */
function handleRegister(e) {
  e.preventDefault();
  const name    = document.getElementById('regName').value.trim();
  const phone   = document.getElementById('regPhone').value.trim();
  const pass    = document.getElementById('regPass').value;
  const confirm = document.getElementById('regPassConfirm').value;
  const terms   = document.getElementById('agreeTerms').checked;

  let valid = true;

  if (!name) {
    showError('nameError', true); setInputError('regName', true); valid = false;
  } else {
    showError('nameError', false); setInputError('regName', false);
  }

  if (!phone || !/^(0|\+84)[0-9]{9}$/.test(phone.replace(/\s/g, ''))) {
    showError('regPhoneError', true); setInputError('regPhone', true); valid = false;
  } else {
    showError('regPhoneError', false); setInputError('regPhone', false);
  }

  if (!pass || pass.length < 8) {
    showError('regPassError', true); setInputError('regPass', true); valid = false;
  } else {
    showError('regPassError', false); setInputError('regPass', false);
  }

  if (pass !== confirm) {
    showError('confirmError', true); setInputError('regPassConfirm', true); valid = false;
  } else {
    showError('confirmError', false); setInputError('regPassConfirm', false);
  }

  if (!terms) {
    showError('termsError', true); valid = false;
  } else {
    showError('termsError', false);
  }

  if (!valid) return;

  const btn = document.getElementById('registerBtn');
  btn.textContent = 'Đang tạo tài khoản...';
  btn.disabled = true;

  setTimeout(() => {
    btn.textContent = 'Tạo tài khoản';
    btn.disabled = false;
    showToast('Đăng ký thành công! Đang chuyển đến đăng nhập...');
    setTimeout(() => { window.location = '/frontend/login.html'; }, 1400);
  }, 1400);
}
