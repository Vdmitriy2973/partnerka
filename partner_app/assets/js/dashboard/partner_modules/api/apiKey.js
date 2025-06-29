export function generateApiKey() {
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
  
  apiKeyShowBtn.addEventListener('click',()=>{
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
    btnCopy.addEventListener('click', () => {
      const apiKey = document.getElementById('api_key').value;
      navigator.clipboard.writeText(apiKey)
        .catch(err => console.error('Copy failed:', err));
    });
  }
}