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

export function setupApiKeyHandlers() {
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
        return;
      }

      const apiKey = apiKeyElement.value;

      if (!apiKey) {
        console.warn('API ключ пустой');
        showAlert('Нет ключа для копирования', 'warning');
        return;
      }

      try {
        await navigator.clipboard.writeText(apiKey);

        // Визуальный фидбек вместо alert()
        showAlert('API ключ скопирован!', 'success');

        // Дополнительный визуальный фидбек на кнопке

        setTimeout(() => {
          btnCopy.innerHTML = '<i class="fas fa-copy"></i>';
        }, 2000);

      } catch (err) {
        console.error('Ошибка копирования:', err);
        showAlert('Не удалось скопировать ключ', 'error');
      }
    });
  }

  // Функция для красивого отображения уведомлений
  function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} fixed top-4 flex justify-center max-w-xs z-50 transition-all text-green-500`;
    alert.innerHTML = `
        <span>${message}</span>
    `;
    document.body.appendChild(alert);

    setTimeout(() => {
      alert.remove();
    }, 3000);
  }
}