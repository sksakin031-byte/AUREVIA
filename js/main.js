(() => {
  'use strict';

  const root = document.documentElement;
  const one = (selector, scope = document) => scope.querySelector(selector);
  const all = (selector, scope = document) => [...scope.querySelectorAll(selector)];
  root.classList.add('js-ready');

  // Responsive primary navigation.
  const menuButton = one('.menu-toggle');
  const primaryNav = one('#primary-nav');
  const closeMenu = () => {
    if (!menuButton || !primaryNav) return;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation');
    primaryNav.classList.remove('is-open');
  };

  if (menuButton && primaryNav) {
    menuButton.addEventListener('click', () => {
      const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'Open navigation' : 'Close navigation');
      primaryNav.classList.toggle('is-open', !isOpen);
    });
    all('a', primaryNav).forEach((link) => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeMenu();
    });
    document.addEventListener('click', (event) => {
      if (!primaryNav.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth > 860) closeMenu();
    });
  }

  // Reveal motion is progressive enhancement; content remains visible without JS.
  const revealItems = all('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -35px 0px' });
    revealItems.forEach((item) => revealObserver.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  }

  // Portfolio category filters.
  const filterButtons = all('[data-filter]');
  const projectCards = all('.project-card[data-category]');
  const filterStatus = one('#filter-status');
  if (filterButtons.length && projectCards.length) {
    filterButtons.forEach((button) => {
      button.addEventListener('click', () => {
        const category = button.dataset.filter;
        let visibleCount = 0;
        projectCards.forEach((card) => {
          const visible = category === 'All' || card.dataset.category === category;
          card.hidden = !visible;
          if (visible) visibleCount += 1;
        });
        filterButtons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
        if (filterStatus) {
          filterStatus.textContent = category === 'All'
            ? `Showing all ${visibleCount} concept studies.`
            : `Showing ${visibleCount} ${category.toLowerCase()} concept ${visibleCount === 1 ? 'study' : 'studies'}.`;
        }
      });
    });
  }

  // The enquiry is a role=form group rather than a submitting <form> element.
  // This guarantees that no user entry can be sent to a server by browser default.
  const enquiry = one('#contact-form[role="form"]');
  const validateButton = one('#validate-enquiry');
  const formStatus = one('#form-status');
  if (enquiry && validateButton && formStatus) {
    const fieldNames = ['name', 'email', 'phone', 'service', 'budget', 'message'];
    const getField = (name) => one(`#${name}`, enquiry);

    const clearFieldError = (name) => {
      const field = getField(name);
      const message = one(`#error-${name}`);
      if (field) field.removeAttribute('aria-invalid');
      if (message) {
        message.textContent = '';
        message.hidden = true;
      }
    };

    const setFieldError = (name, text) => {
      const field = getField(name);
      const message = one(`#error-${name}`);
      if (field) field.setAttribute('aria-invalid', 'true');
      if (message) {
        message.textContent = text;
        message.hidden = false;
      }
    };

    const validate = () => {
      const values = Object.fromEntries(fieldNames.map((name) => [name, (getField(name)?.value || '').trim()]));
      const errors = {};

      if (values.name.length < 2) errors.name = 'Please enter at least 2 characters for your name.';
      if (values.name.length > 100) errors.name = 'Please keep your name under 100 characters.';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email) || values.email.length > 254) {
        errors.email = 'Enter a valid email address.';
      }
      if (values.phone) {
        const digits = values.phone.replace(/\D/g, '');
        if (!/^\+?[\d\s().-]+$/.test(values.phone) || digits.length < 7 || digits.length > 15) {
          errors.phone = 'Enter a phone number with 7–15 digits, or leave this field blank.';
        }
      }
      if (!values.service) errors.service = 'Choose a service or select “Still shaping the brief”.';
      if (!values.budget) errors.budget = 'Choose a budget range or “Not decided yet”.';
      if (values.message.length < 10) errors.message = 'Please add at least 10 characters about the project.';
      if (values.message.length > 2000) errors.message = 'Please keep the description under 2,000 characters.';

      fieldNames.forEach((name) => {
        if (errors[name]) setFieldError(name, errors[name]);
        else clearFieldError(name);
      });

      formStatus.classList.remove('is-success', 'is-error');
      if (Object.keys(errors).length) {
        formStatus.textContent = 'Please review the highlighted fields. This demo will not send your information.';
        formStatus.classList.add('is-error');
        getField(Object.keys(errors)[0])?.focus();
        return;
      }

      formStatus.textContent = 'Your enquiry looks complete. This fictional demo does not send, email or store it.';
      formStatus.classList.add('is-success');
    };

    fieldNames.forEach((name) => {
      const field = getField(name);
      if (!field) return;
      const eventName = field.tagName === 'SELECT' ? 'change' : 'input';
      field.addEventListener(eventName, () => {
        clearFieldError(name);
        formStatus.textContent = '';
        formStatus.classList.remove('is-success', 'is-error');
      });
    });

    validateButton.addEventListener('click', validate);
    enquiry.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' && event.target.tagName !== 'TEXTAREA' && event.target.tagName !== 'SELECT') {
        event.preventDefault();
        validate();
      }
    });
  }

  // Back-to-top control and current year.
  const topButton = one('#back-to-top');
  if (topButton) {
    const updateTopButton = () => topButton.classList.toggle('is-visible', window.scrollY > 500);
    window.addEventListener('scroll', updateTopButton, { passive: true });
    updateTopButton();
    topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  const year = one('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
