function generateApiKey() {
  const prefix = 'sk-';
  const length = 25;
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789';

  const crypto = window.crypto || window.msCrypto;
  const values = new Uint32Array(length);
  crypto.getRandomValues(values);

  let key = prefix;
  for (let i = 0; i < length; i++) {
    key += chars[values[i] % chars.length];
  }

  return key;
}

export function setupApiKeySettings() {
  const btnGenerate = document.getElementById('generate_api_key');
  const btnCopy = document.getElementById('copy_api_key');

  const apiKeyInput = document.getElementById('api_key');
  const apiKeyShowBtn = document.getElementById('show_api_key');

  apiKeyShowBtn.addEventListener('click', () => {
    if (apiKeyInput.type === 'password') {
      apiKeyInput.type = 'text';
    } else {
      apiKeyInput.type = 'password';
    }
  })


  if (btnGenerate) {
    btnGenerate.addEventListener('click', () => {
      document.getElementById('api_key').value = generateApiKey();
    });
  }

  if (btnCopy) {
    btnCopy.addEventListener('click', async () => {
      const apiKeyElement = document.getElementById('api_key');

      if (!apiKeyElement) {
        console.error('Элемент с API ключом не найден');
        showAlert('Ошибка: поле с ключом не найдено', 'error');
        return;
      }

      const apiKey = apiKeyElement.value;

      if (!apiKey) {
        console.warn('API ключ пустой');
        showAlert('Нет ключа для копирования', 'warning');
        return;
      }

      // Проверка поддержки Clipboard API
      if (!navigator.clipboard) {
        console.warn('Clipboard API не поддерживается');
        fallbackCopy(apiKey);
        return;
      }

      try {
        await navigator.clipboard.writeText(apiKey);
        showAlert('API ключ скопирован!', 'success');
        updateButtonState(btnCopy, true);
      } catch (err) {
        console.error('Ошибка копирования:', err);
        fallbackCopy(apiKey);
      }
    });
  }

  // Резервный метод копирования
  function fallbackCopy(text) {
    try {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed'; // Невидимый элемент
      document.body.appendChild(textarea);
      textarea.select();

      const successful = document.execCommand('copy');
      document.body.removeChild(textarea);

      if (successful) {
        showAlert('API ключ скопирован', 'success');
      } else {
        throw new Error('Резервное копирование не удалось');
      }
    } catch (err) {
      console.error('Резервное копирование не удалось:', err);
      showAlert('Не удалось скопировать ключ. Скопируйте вручную.', 'error');
    }
  }

  // Обновление состояния кнопки
  function updateButtonState(button, success) {
    if (success) {
      button.innerHTML = '<i class="fas fa-check"></i>';
      button.classList.add('btn-success');
      setTimeout(() => {
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.classList.remove('btn-success');
      }, 2000);
    } else {
      button.innerHTML = '<i class="fas fa-times"></i> Ошибка';
      button.classList.add('btn-error');
      setTimeout(() => {
        button.innerHTML = '<i class="fas fa-copy"></i> Копировать';
        button.classList.remove('btn-error');
      }, 2000);
    }
  }
  function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} fixed top-4 flex justify-center max-w-xs z-50 text-white p-4 mb-6 transition-all duration-300 ease-out shadow-lg animate-fade-in`;
    const iconClass = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
    alert.innerHTML = `<i class="fas ${iconClass} mr-2"></i>${message}`;
    document.body.appendChild(alert);

    setTimeout(() => {
      alert.classList.add('opacity-0', 'translate-y-[-20px]');
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  }
}