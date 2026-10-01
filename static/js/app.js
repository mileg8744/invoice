document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((el) => {
    setTimeout(() => {
      el.classList.add("fade");
    }, 6000);
  });

  const KEY = "pgu.sidebarCollapsed";
  const hideBtn = document.getElementById("btnHideSidebar");
  const showBtn = document.getElementById("btnShowSidebar");
  const restoreBtn = document.getElementById("btnRestoreSidebar");

  function setCollapsed(collapsed) {
    document.documentElement.classList.toggle("sidebar-collapsed", collapsed);
    try {
      localStorage.setItem(KEY, collapsed ? "1" : "0");
    } catch (e) {}
  }

  hideBtn?.addEventListener("click", () => setCollapsed(true));
  showBtn?.addEventListener("click", () => setCollapsed(false));
  restoreBtn?.addEventListener("click", () => setCollapsed(false));

  bindAddressSearch();
});

function bindAddressSearch() {
  const boxes = document.querySelectorAll(".addr-search");
  if (!boxes.length) return;

  boxes.forEach((box) => {
    const input = box.querySelector(".js-addr-q");
    const results = box.querySelector(".js-addr-results");
    const target = box.querySelector(".js-addr-target");
    const daumBtn = box.querySelector(".js-addr-daum");
    const noneText = box.getAttribute("data-empty") || "검색 결과가 없습니다.";
    const countryInput = box.closest("form")?.querySelector('[name="country_en"]');
    let timer = null;
    let seq = 0;

    function hideResults() {
      results.hidden = true;
      results.innerHTML = "";
    }

    function showItems(items) {
      results.innerHTML = "";
      if (!items.length) {
        const li = document.createElement("li");
        li.className = "addr-empty";
        li.textContent = noneText;
        results.appendChild(li);
        results.hidden = false;
        return;
      }
      items.forEach((item) => {
        const li = document.createElement("li");
        const btn = document.createElement("button");
        btn.type = "button";
        btn.innerHTML = `<span>${escapeHtml(item.label).replace(/\n/g, "<br>")}</span>`;
        if (item.detail && item.detail !== item.label) {
          const small = document.createElement("small");
          small.textContent = item.detail;
          btn.appendChild(small);
        }
        btn.addEventListener("click", () => {
          target.value = item.label;
          input.value = "";
          hideResults();
          target.focus();
        });
        li.appendChild(btn);
        results.appendChild(li);
      });
      results.hidden = false;
    }

    async function runSearch(query) {
      const current = ++seq;
      try {
        const country = (countryInput?.value || box.getAttribute("data-country") || "").trim();
        const url = `/api/address-search?q=${encodeURIComponent(query)}&country=${encodeURIComponent(country)}`;
        const res = await fetch(url, { headers: { Accept: "application/json" } });
        const data = await res.json();
        if (current !== seq) return;
        showItems((data && data.items) || []);
      } catch (e) {
        if (current !== seq) return;
        showItems([]);
      }
    }

    input?.addEventListener("input", () => {
      const query = (input.value || "").trim();
      clearTimeout(timer);
      if (query.length < 3) {
        hideResults();
        return;
      }
      timer = setTimeout(() => runSearch(query), 350);
    });

    input?.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") {
        ev.preventDefault();
        clearTimeout(timer);
        const query = (input.value || "").trim();
        if (query.length >= 3) runSearch(query);
        const country = (countryInput?.value || box.getAttribute("data-country") || "").toLowerCase();
        if (/^\d{5}$/.test(query) && /korea|대한민국|한국/.test(country)) {
          daumBtn?.click();
        }
      }
      if (ev.key === "Escape") hideResults();
    });

    document.addEventListener("click", (ev) => {
      if (!box.contains(ev.target)) hideResults();
    });

    daumBtn?.addEventListener("click", () => {
      loadDaumPostcode(() => {
        new window.daum.Postcode({
          oncomplete(data) {
            const english = data.roadAddressEnglish || data.addressEnglish || data.jibunAddressEnglish || "";
            const zip = data.zonecode || "";
            const building = data.buildingName ? `, ${data.buildingName}` : "";
            target.value = [english + building, zip].filter(Boolean).join("\n");
            input.value = "";
            hideResults();
          },
        }).open();
      });
    });
  });
}

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function loadDaumPostcode(done) {
  if (window.daum && window.daum.Postcode) {
    done();
    return;
  }
  const existing = document.getElementById("daum-postcode-sdk");
  if (existing) {
    existing.addEventListener("load", () => done(), { once: true });
    return;
  }
  const script = document.createElement("script");
  script.id = "daum-postcode-sdk";
  script.src = "https://t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js";
  script.onload = () => done();
  document.head.appendChild(script);
}
