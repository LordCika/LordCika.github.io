document.addEventListener("DOMContentLoaded", function () {
  const firma = document.getElementById("firma-articolo");
  if (firma) {
    firma.innerHTML = `
      <div style="
        margin-top: 56px;
        padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.12);
        font-size: 14px;
        color: rgba(255,255,255,0.72);
      ">
        Firmato da
        <a
          href=https://www.facebook.com/zavathalavudvash"
          target="_blank"
          rel="noopener noreferrer"
          style="
            color: #ffffff;
            text-decoration: none;
            font-weight: 600;
            margin-left: 4px;
            transition: opacity 0.2s ease;
          "
          onmouseover="this.style.opacity='0.75'"
          onmouseout="this.style.opacity='1'"
        >
          Marco Di Capua
        </a>
      </div>
    `;
  }
});
