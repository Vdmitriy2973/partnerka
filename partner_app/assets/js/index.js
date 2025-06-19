import "tailwindcss"
import 'vite/modulepreload-polyfill'
import '@fortawesome/fontawesome-free/js/all'
import './base.js'
import '../css/index.css.js'


// Hero section
// Tab switching functionality
const adv_tab = document.getElementById("advertiser-tab");
adv_tab.addEventListener("click",()=>{
  switchTab("advertiser");
})

const partner_tab = document.getElementById("partner-tab");
partner_tab.addEventListener("click",()=>{
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
