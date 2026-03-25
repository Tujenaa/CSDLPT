/* ─────────────────────────────────
   PROFILE.JS
───────────────────────────────── */

/* ── TOAST (shared) ── */
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 2800);
}

/* ── NAVBAR DROPDOWN ── */
function toggleDropdown() {
  const dd = document.getElementById('profileDropdown');
  dd.classList.toggle('show');
}
document.addEventListener('click', (e) => {
  const wrap = document.querySelector('.profile-dropdown-wrap');
  if (wrap && !wrap.contains(e.target)) {
    document.getElementById('profileDropdown')?.classList.remove('show');
  }
});

/* ── LOGOUT ── */
function handleLogout() {
  showToast('Đang đăng xuất...');
  setTimeout(() => { window.location = '/frontend/login.html'; }, 1000);
}

/* ── SIDEBAR TABS ── */
function switchTab(btn, tabName) {
  // Update sidebar active state
  document.querySelectorAll('.sidebar-nav-item').forEach(el => el.classList.remove('active'));
  btn.classList.add('active');

  // Show/hide tab panels
  ['info', 'stats', 'security'].forEach(name => {
    const el = document.getElementById('tab-' + name);
    if (el) el.style.display = name === tabName ? 'flex' : 'none';
  });
  const active = document.getElementById('tab-' + tabName);
  if (active) active.style.display = 'block';
}

/* ── EDIT INFO ── */
let isEditing = false;
const fields = ['name', 'phone', 'email', 'dob', 'address'];

function toggleEdit() {
  isEditing = !isEditing;
  fields.forEach(f => {
    document.getElementById('val-' + f).style.display = isEditing ? 'none' : 'block';
    document.getElementById('inp-' + f).style.display = isEditing ? 'block' : 'none';
  });
  const btn = document.getElementById('editInfoBtn');
  btn.classList.toggle('active', isEditing);
  btn.innerHTML = isEditing
    ? `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg> Huỷ`
    : `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg> Chỉnh sửa`;
  document.getElementById('formActions').style.display = isEditing ? 'flex' : 'none';

  if (!isEditing) {
    // Restore values when cancelling via button
  }
}

function cancelEdit() {
  isEditing = true; // flip so toggleEdit sets it to false
  toggleEdit();
}

function saveInfo() {
  fields.forEach(f => {
    const inp = document.getElementById('inp-' + f);
    const val = document.getElementById('val-' + f);
    val.textContent = inp.value || val.textContent;
  });
  isEditing = true;
  toggleEdit();
  showToast('Thông tin đã được cập nhật!');
}

/* ── AVATAR PREVIEW ── */
function previewAvatar(input) {
  if (!input.files || !input.files[0]) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    document.getElementById('sidebarAvatar').src = e.target.result;
    // Also update navbar avatar if present
    const navAvatar = document.querySelector('.navbar .profile-avatar');
    if (navAvatar) navAvatar.src = e.target.result;
    showToast('Ảnh đại diện đã được cập nhật!');
  };
  reader.readAsDataURL(input.files[0]);
}
