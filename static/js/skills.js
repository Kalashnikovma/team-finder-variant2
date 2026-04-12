(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', () => {
        const addBtn = document.getElementById('add-skill-btn');
        const input = document.getElementById('skill-input');
        const container = document.getElementById('skills-list-container');
        const datalist = document.getElementById('skills-list');

        if (!addBtn || !input || !container) return;

        addBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();

            const skillName = input.value.trim();
            const userId = input.dataset.userId;

            if (!skillName) {
                alert('Введите название навыка');
                return;
            }

            try {
                const res = await fetch('/users/ajax/add-skill/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ skill_name: skillName, user_id: userId })
                });

                const data = await res.json();

                if (res.ok && data.success) {
                    appendSkillChip(data.skill.user_skill_id, data.skill.name);
                    input.value = '';
                    if (datalist) datalist.innerHTML = '';
                } else {
                    alert(data.error || 'Не удалось добавить навык');
                }
            } catch (err) {
                console.error(err);
                alert('Ошибка соединения с сервером');
            }
        });

        container.addEventListener('click', async (e) => {
            const removeBtn = e.target.closest('.remove-skill-btn');
            if (!removeBtn) return;

            e.preventDefault();
            if (!confirm('Удалить этот навык?')) return;

            const userSkillId = removeBtn.dataset.userSkillId;
            const chip = removeBtn.closest('.skill-tag');

            try {
                const res = await fetch(`/users/ajax/remove-skill/${userSkillId}/`, {
                    method: 'DELETE',
                    headers: { 'X-CSRFToken': getCSRFToken() }
                });

                if (res.ok) {
                    chip.remove();
                    if (container.querySelectorAll('.skill-tag').length === 0) {
                        container.innerHTML = '<p class="no-skills">Пока нет добавленных навыков</p>';
                    }
                } else {
                    alert('Ошибка при удалении');
                }
            } catch (err) {
                console.error(err);
            }
        });
    });

    function appendSkillChip(id, name) {
        const container = document.getElementById('skills-list-container');
        const emptyMsg = container.querySelector('.no-skills');
        if (emptyMsg) emptyMsg.remove();

        const chip = document.createElement('div');
        chip.className = 'skill-tag';
        chip.dataset.userSkillId = id;
        chip.innerHTML = `<span>${name}</span><button type="button" class="remove-skill-btn" data-user-skill-id="${id}">×</button>`;
        container.appendChild(chip);
    }

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