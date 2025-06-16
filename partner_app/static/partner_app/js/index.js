// Hero section
// Tab switching functionality
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
