'use strict';

const all = (selector, root = document) => Array.from(root.querySelectorAll(selector));
const first = (selector, root = document) => root.querySelector(selector);

window.addEventListener('load', () => {
  window.setTimeout(() => all('#ld').forEach((loader) => loader.classList.add('h')), 250);
});

const burger = first('.burger');
const navMenu = first('.nav ul');
if (burger && navMenu) {
  const closeMenu = () => {
    navMenu.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
  };
  burger.addEventListener('click', () => {
    const willOpen = burger.getAttribute('aria-expanded') !== 'true';
    navMenu.classList.toggle('open', willOpen);
    burger.setAttribute('aria-expanded', String(willOpen));
  });
  all('.nav a', navMenu).forEach((link) => link.addEventListener('click', closeMenu));
}

if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  all('.rv').forEach((element) => revealObserver.observe(element));
} else {
  all('.rv').forEach((element) => element.classList.add('in'));
}

const backToTop = first('#top');
if (backToTop) {
  window.addEventListener('scroll', () => backToTop.classList.toggle('show', window.scrollY > 500));
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

all('.filters button').forEach((filterButton) => {
  filterButton.addEventListener('click', () => {
    all('.filters button').forEach((button) => button.classList.remove('on'));
    filterButton.classList.add('on');
    const category = filterButton.dataset.f || 'All';
    all('[data-c]').forEach((card) => {
      card.hidden = category !== 'All' && card.dataset.c !== category;
    });
  });
});

all('.acc button').forEach((question) => {
  question.addEventListener('click', () => {
    const answer = question.nextElementSibling;
    if (!answer) return;
    const isOpen = question.getAttribute('aria-expanded') === 'true';
    question.setAttribute('aria-expanded', String(!isOpen));
    answer.style.maxHeight = isOpen ? '0px' : `${answer.scrollHeight}px`;
    if (question.lastElementChild) question.lastElementChild.textContent = isOpen ? '+' : '−';
  });
});

const form = first('#cf');
if (form) {
  const fieldIds = ['name', 'email', 'phone', 'service', 'budget', 'message'];
  const status = first('#note', form);
  let hasAttemptedSubmit = false;

  const validateField = (field) => {
    const value = field.value.trim();
    switch (field.id) {
      case 'name':
        return value.length < 2 ? 'Please enter at least 2 characters for your name.' : '';
      case 'email':
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value) ? '' : 'Enter a valid email address.';
      case 'phone': {
        if (!value) return '';
        const digits = value.replace(/\D/g, '').length;
        return /^\+?[\d\s().-]+$/.test(value) && digits >= 7 && digits <= 15
          ? ''
          : 'Enter a valid phone number, including country code if useful, or leave it blank.';
      }
      case 'service':
        return value ? '' : 'Choose a service of interest.';
      case 'budget':
        return value ? '' : 'Choose an estimated project budget.';
      case 'message':
        return value.length < 10 ? 'Please add at least 10 characters about your project.' : '';
      default:
        return '';
    }
  };

  const updateFieldError = (field) => {
    const error = validateField(field);
    const errorElement = first(`#e-${field.id}`, form);
    if (errorElement) {
      errorElement.textContent = error;
      errorElement.hidden = !error;
    }
    field.setAttribute('aria-invalid', String(Boolean(error)));
    return error;
  };

  const hideStatus = () => {
    if (!status) return;
    status.textContent = '';
    status.classList.remove('on');
    status.hidden = true;
  };

  const refreshAfterEdit = (event) => {
    const field = event.target;
    if (!fieldIds.includes(field.id)) return;
    hideStatus();
    if (hasAttemptedSubmit) updateFieldError(field);
  };
  form.addEventListener('input', refreshAfterEdit);
  form.addEventListener('change', refreshAfterEdit);

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    hasAttemptedSubmit = true;
    const fields = fieldIds.map((id) => first(`#${id}`, form)).filter(Boolean);
    const invalidFields = fields.filter((field) => updateFieldError(field));

    if (invalidFields.length) {
      if (status) {
        status.textContent = 'Please review the highlighted fields and try again.';
        status.hidden = false;
        status.classList.add('on');
      }
      invalidFields[0].focus();
      return;
    }

    if (status) {
      status.textContent = 'Your details look complete. This demo does not send or store enquiries.';
      status.hidden = false;
      status.classList.add('on');
      status.focus();
    }
  });
}
