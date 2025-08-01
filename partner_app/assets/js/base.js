import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'

// -----------------------------
// 🔗 Smooth scrolling
// -----------------------------
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", (e) => {
    e.preventDefault();
    const targetId = anchor.getAttribute("href");
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: "smooth" });
    }
  });
});


// -----------------------------
// 📌 Navbar scroll effect
// -----------------------------
window.addEventListener("scroll", () => {
  const navbar = document.getElementById("navbar");
  navbar?.classList.toggle("scrolled", window.scrollY > 50);
});




// -----------------------------
// 🧩 Modal open/close
// -----------------------------


let currentType = "partner";

// Авторизация
const authBtn = document.getElementById("authModal");
if (authBtn) {
  authBtn.addEventListener("click", () => {
    openModal("auth");
  });
}

// Регистрация
const regPartnerBtn = document.getElementById("reg_partner-btn");
if (regPartnerBtn) {
  regPartnerBtn.addEventListener("click", () => {
    openModal('register', 'partner');
  })
}


const regAdvertiserBtn = document.getElementById("reg_advertiser-btn");
if (regAdvertiserBtn) {
  regAdvertiserBtn.addEventListener("click", () => {
    openModal('register', 'advertiser');
  })
}

// Вкладка партнёра
const partnerTab = document.getElementById("tab-partner");
if (partnerTab) {
  partnerTab.addEventListener("click", () => {
    openModal('register', 'partner');
  })
}

// Вкладка рекламодателя
const advertiserTab = document.getElementById("tab-advertiser");
if (advertiserTab) {
  advertiserTab.addEventListener("click", () => {
    openModal('register', 'advertiser');
  })
}

// Вкладка регистрации
const registrationLink = document.getElementById("registration-link");
if (registrationLink) {
  registrationLink.addEventListener("click", () => {
    closeModal('auth');
    openModal('register', 'partner')
  })
}
// Вкладка авторизации
const authorizationLink = document.getElementById("authorization-Link");
if (authorizationLink) {
  authorizationLink.addEventListener("click", () => {
    closeModal('register');
    openModal('auth');
  });
}

function openModal(type, userType = "partner") {
  if (type === "register") {
    currentType = userType;
    switchModalTab(userType);
  }
  document.getElementById(`${type}_modal`).showModal();
}

function closeModal(type) {
  document.getElementById(`${type}_modal`).close();
}


// -----------------------------
// 🔄 Tab switch logic
// -----------------------------
function switchModalTab(type) {

  const tabs = {
    partner: document.getElementById("tab-partner"),
    advertiser: document.getElementById("tab-advertiser"),
  };

  const forms = {
    partner: document.getElementById("form-partner"),
    advertiser: document.getElementById("form-advertiser"),
  };

  Object.keys(tabs).forEach((key) => {
    const isActive = key === type;

    tabs[key].classList.toggle("tab-active", isActive);
    forms[key].classList.toggle("hidden", !isActive);
    forms[key].classList.toggle("active_reg-form", isActive);
  });

  // Обновление UI под тип пользователя
  const regHeader = document.getElementById("reg-header");
  const old_icon = document.getElementById("reg-icon");

  old_icon.parentNode.removeChild(old_icon);

  const icon = document.createElement("i");

  const title = document.getElementById("reg-title");
  const subtitle = document.getElementById("reg-subtitle");

  const config = {
    partner: {
      icon: "fas fa-user-plus text-4xl text-blue-600 mb-4",
      title: "Регистрация партнёра",
      subtitle: "Начните зарабатывать с нами",
      width: 40
    },
    advertiser: {
      icon: "fas fa-bullhorn text-4xl text-green-500 mb-4",
      title: "Регистрация рекламодателя",
      subtitle: "Привлекайте новых клиентов"
    },
  }[type];


  icon.setAttribute("class", config.icon);
  icon.id = "reg-icon";
  regHeader.prepend(icon);

  icon.style.margin = "0 auto";
  title.textContent = config.title;
  subtitle.textContent = config.subtitle;
}


const msg = document.querySelector('.alert');
if (msg) {
  setTimeout(function () {
    msg.remove()
  }, 5000)
}