document.addEventListener('DOMContentLoaded', () => {
  const resilientImages = Array.from(document.querySelectorAll('img[data-fallback-src]'));
  resilientImages.forEach((image) => {
    image.addEventListener('error', () => {
      const fallbackSrc = image.dataset.fallbackSrc;
      if (!fallbackSrc || image.dataset.fallbackApplied === 'true') return;
      image.dataset.fallbackApplied = 'true';
      image.classList.add('is-fallback-icon');
      image.src = fallbackSrc;
    });
  });

  const details = Array.from(document.querySelectorAll('.accordion'));
  const openAll = document.querySelector('[data-open-all]');
  const closeAll = document.querySelector('[data-close-all]');

  if (openAll) {
    openAll.addEventListener('click', () => details.forEach(item => item.open = true));
  }
  if (closeAll) {
    closeAll.addEventListener('click', () => details.forEach(item => item.open = false));
  }

  const tabs = Array.from(document.querySelectorAll('[data-role-tab]'));
  const panels = Array.from(document.querySelectorAll('[data-role-panel]'));
  const board = document.querySelector('[data-role-order]');
  const navButtons = Array.from(document.querySelectorAll('[data-role-nav]'));

  if (tabs.length && panels.length) {
    const roleOrder = board ? JSON.parse(board.dataset.roleOrder) : tabs.map((tab) => tab.dataset.roleTab);

    const updateUrl = (role) => {
      if (!window.history || !window.history.replaceState) return;
      const url = new URL(window.location.href);
      url.searchParams.set('role', role);
      window.history.replaceState({}, '', url);
    };

    const activateRole = (role) => {
      tabs.forEach((tab) => {
        const isActive = tab.dataset.roleTab === role;
        tab.classList.toggle('is-active', isActive);
        tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      panels.forEach((panel) => {
        const isActive = panel.dataset.rolePanel === role;
        panel.classList.toggle('is-active', isActive);
        panel.hidden = !isActive;
      });

      updateUrl(role);
    };

    const moveRole = (direction) => {
      const activeTab = tabs.find((tab) => tab.classList.contains('is-active')) || tabs[0];
      const currentRole = activeTab.dataset.roleTab;
      const currentIndex = roleOrder.indexOf(currentRole);
      const delta = direction === 'next' ? 1 : -1;
      const nextIndex = (currentIndex + delta + roleOrder.length) % roleOrder.length;
      activateRole(roleOrder[nextIndex]);
    };

    tabs.forEach((tab) => {
      tab.addEventListener('click', () => activateRole(tab.dataset.roleTab));
    });

    navButtons.forEach((button) => {
      button.addEventListener('click', () => moveRole(button.dataset.roleNav));
    });
  }
});
