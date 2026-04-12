(function(){
  document.addEventListener("DOMContentLoaded", function() {
    const completeBtn = document.getElementById("complete-project-btn");
    if (completeBtn) {
      completeBtn.addEventListener("click", function(e) {
        e.preventDefault();
        const projectId = completeBtn.dataset.id;
        if (!projectId) return;
        if (!confirm("Завершить проект?")) return;

        const csrfToken = getCSRFToken();
        fetch(`/projects/${projectId}/complete/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
          }
        }).finally(() => {
          location.reload();
        });
      });
    }

    const participateBtn = document.getElementById("participate-btn");
    if (participateBtn) {
      participateBtn.addEventListener("click", function(e) {
        e.preventDefault();
        const projectId = participateBtn.dataset.project;
        if (!projectId) return;

        const csrfToken = getCSRFToken();
        fetch(`/projects/${projectId}/toggle-participate/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({})
        }).finally(() => {
          location.reload();
        });
      });
    }
  });

  function getCSRFToken() {
    const name = 'csrftoken';
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
})();