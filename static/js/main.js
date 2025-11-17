document.addEventListener('DOMContentLoaded', function () {
  const newPostForm = document.getElementById('new-post-form');
  const postsList = document.querySelector('.list-group');

  // CSRF helper: get cookie value
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  // Helper: send fetch with form data, return JSON
  async function postForm(url, formData) {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrftoken},
      body: formData
    });
    return resp.json();
  }

  // Create post via AJAX
  if (newPostForm && postsList) {
    newPostForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      const fd = new FormData(newPostForm);
      const url = window.location.pathname;
      try {
        const data = await postForm(url, fd);
        if (data.success && data.html) {
          // prepend new item
          postsList.insertAdjacentHTML('afterbegin', data.html);
          // clear textarea
          const ta = newPostForm.querySelector('textarea'); if (ta) ta.value = '';
          // show toast
          showToast('Post created', 'success');
          // rebind buttons
          bindPostButtons();
        } else if (data.errors) {
          showToast('Error creating post', 'danger');
        }
      } catch (err) {
        console.error(err);
        showToast('Error creating post', 'danger');
      }
    });
  }

  // Modal elements
  const editModalEl = document.getElementById('editModal');
  const editModal = editModalEl ? new bootstrap.Modal(editModalEl) : null;
  const editModalBody = editModalEl ? editModalEl.querySelector('.modal-body') : null;
  const deleteModalEl = document.getElementById('deleteModal');
  const deleteModal = deleteModalEl ? new bootstrap.Modal(deleteModalEl) : null;
  const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
  let pendingDeleteUrl = null;
  let pendingDeletePk = null;

  // Bind edit/delete buttons
  function bindPostButtons() {
    document.querySelectorAll('.btn-edit').forEach(btn => {
      btn.removeEventListener('click', onEditClick);
      btn.addEventListener('click', onEditClick);
    });
    document.querySelectorAll('.btn-delete').forEach(btn => {
      btn.removeEventListener('click', onDeleteClick);
      btn.addEventListener('click', onDeleteClick);
    });
  }

  async function onEditClick(e) {
    const url = e.currentTarget.dataset.editUrl;
    // fetch form via GET
    const resp = await fetch(url, {headers: {'X-Requested-With': 'XMLHttpRequest'}});
    const data = await resp.json();
    if (data.form_html) {
      editModalBody.innerHTML = data.form_html;
      editModal.show();
      // bind form submit
      const form = editModalBody.querySelector('form');
      form.addEventListener('submit', async function (ev) {
        ev.preventDefault();
        const fd = new FormData(form);
        const postUrl = url; // same URL handles POST
        const resp2 = await fetch(postUrl, {method: 'POST', headers: {'X-Requested-With': 'XMLHttpRequest'}, body: fd});
        const data2 = await resp2.json();
        if (data2.success && data2.html) {
          // replace item
          const tmp = document.createElement('div'); tmp.innerHTML = data2.html;
          const newNode = tmp.firstElementChild;
          const old = document.getElementById('post-' + newNode.id.split('-')[1]);
          if (old) old.replaceWith(newNode);
          editModal.hide();
          bindPostButtons();
        } else if (data2.errors) {
          alert('Error: ' + data2.errors);
        }
      });
    }
  }

  async function onDeleteClick(e) {
    pendingDeleteUrl = e.currentTarget.dataset.deleteUrl;
    // infer pk from url (last segment)
    const parts = pendingDeleteUrl.split('/').filter(Boolean);
    pendingDeletePk = parts[parts.length - 2] || null; // expecting /post/<pk>/delete/
    if (deleteModal) deleteModal.show();
  }

  // confirm delete handler
  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener('click', async function () {
      if (!pendingDeleteUrl) return;
      try {
        const resp = await fetch(pendingDeleteUrl, {method: 'POST', headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrftoken}, body: new FormData()});
        const data = await resp.json();
        if (data.success) {
          const el = document.getElementById('post-' + data.pk);
          if (el) el.remove();
          showToast('Post deleted', 'success');
        } else {
          showToast('Could not delete post', 'danger');
        }
      } catch (err) {
        console.error(err);
        showToast('Could not delete post', 'danger');
      } finally {
        if (deleteModal) deleteModal.hide();
        pendingDeleteUrl = null; pendingDeletePk = null;
      }
    });
  }

  // initial bind
  bindPostButtons();

  // Toast helper
  function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
      <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body">${message}</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>`;
    container.insertAdjacentHTML('beforeend', toastHtml);
    const toastEl = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastEl, {delay: 2500});
    bsToast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
  }

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Fade in elements on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe all list items for fade-in effect
  document.querySelectorAll('.list-group-item').forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(20px)';
    item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(item);
  });

  // Add entrance animation to cards
  document.querySelectorAll('.card').forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 100);
  });
});
