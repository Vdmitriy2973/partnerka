import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import './base.js'
import '../css/index.css'


// Hero section
// Tab switching functionality
const adv_tab = document.getElementById("advertiser-tab");
adv_tab.addEventListener("click", () => {
  switchTab("advertiser");
})

const partner_tab = document.getElementById("partner-tab");
partner_tab.addEventListener("click", () => {
  switchTab("partner");
})

function switchTab(tabType) {
  // Remove active class from all tabs and content
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.remove("tab-active");
  });
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.remove("active");
  });

  // Add active class to selected tab and content
  document.getElementById(tabType + "-tab").classList.add("tab-active");
  document.getElementById(tabType + "-content").classList.add("active");
}

const urlParams = new URLSearchParams(window.location.search);

function openModalReg(type = 'partner') {
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

  setTimeout(() => {
    document.getElementById('register_modal').showModal();
  }, 505)
}

let type = urlParams.get('show_modal');

if (type == "auth") {
  window.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
      document.getElementById(`auth_modal`).showModal();
    }, 505)
  });
}
else if(type == "partner" || type == "advertiser")
{
  openModalReg(type);
}


const becomePartnerBtn = document.getElementById("become_partner");
becomePartnerBtn.addEventListener("click",()=>{
  openModalReg("partner");
})

const becomeAdvertiserBtn = document.getElementById("become_advertiser");
becomeAdvertiserBtn.addEventListener("click",()=>{
  openModalReg("advertiser");
})