  // -----------------------------
  // 🔗 Smooth scrolling
  // -----------------------------
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (e) => {
      e.preventDefault();
      const targetId = anchor.getAttribute("href");
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  // -----------------------------
  // 📌 Navbar scroll effect
  // -----------------------------
  window.addEventListener("scroll", () => {
    const navbar = document.getElementById("navbar");
    navbar.classList.toggle("scrolled", window.scrollY > 50);
  });

  // -----------------------------
  // 🧩 Modal open/close
  // -----------------------------
  let currentType = "partner";

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
  // ✅ Agreement checkbox control
  // -----------------------------
  const checkboxAgreement = document.getElementById("checkbox_agreement");
  const registerBtn = document.getElementById("reg-btn");

  checkboxAgreement.addEventListener("change", () => {
    registerBtn.disabled = !checkboxAgreement.checked;
  });

  // -----------------------------
  // 📤 Submit active form
  // -----------------------------

  function validateForm(form) {
    // Выбираем все input, select в форме, кроме скрытых
    const inputs = form.querySelectorAll('input:not([type="hidden"]), select');
    for (let input of inputs) {
      // Проверяем, пустое ли значение (trim, чтобы убрать пробелы)
      if (!input.value.trim()) {
        return false; // остановить отправку формы
      }
    }
    return true; // все заполнено
  }

  registerBtn.addEventListener("click", () => {
    const activeForm = document.querySelector(".active_reg-form");

    if (validateForm(activeForm)) {
      activeForm?.submit();
    }
    else {
      const regForm = document.getElementById("register-form");
      const infoMsg = document.createElement("div");
      infoMsg.classList.add("text-center", "text-red-500");
      const infoMsgContent = document.createTextNode("Все поля должны быть заполнены!");
      infoMsg.appendChild(infoMsgContent);
      regForm.append(infoMsg);
    }
  });

  // -----------------------------
  // 🔄 Tab switch logic
  // -----------------------------
  function switchModalTab(type) {
    currentType = type;

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
    const icon = document.getElementById("reg-icon");
    const title = document.getElementById("reg-title");
    const subtitle = document.getElementById("reg-subtitle");
    const btn = document.getElementById("reg-btn");

    const config = {
      partner: {
        icon: "fas fa-user-tie text-4xl text-blue-600 mb-4",
        title: "Регистрация партнёра",
        subtitle: "Начните зарабатывать с нами",
        btnHtml: '<i class="fas fa-user-tie mr-2"></i>Зарегистрироваться как партнёр',
        btnClass: "btn gradient-bg text-white w-full hover:scale-105 transition-all hover-lift",
      },
      advertiser: {
        icon: "fas fa-bullhorn text-4xl text-green-600 mb-4",
        title: "Регистрация рекламодателя",
        subtitle: "Привлекайте новых клиентов",
        btnHtml: '<i class="fas fa-bullhorn mr-2"></i>Зарегистрироваться как рекламодатель',
        btnClass: "btn bg-green-600 hover:bg-green-700 text-white w-full hover:scale-105 transition-all hover-lift",
      },
    }[type];

    icon.className = config.icon;
    title.textContent = config.title;
    subtitle.textContent = config.subtitle;
    btn.innerHTML = config.btnHtml;
    btn.className = config.btnClass;
  }
