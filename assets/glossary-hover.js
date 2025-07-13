document.addEventListener("DOMContentLoaded", function () {
    const glossaryUrl = window.location.hostname === "localhost"
        ? "/assets/glossary.json"
        : "/docs-understanding-map/assets/glossary.json";
    const tooltipClass = "glossary-tooltip";

    // Create reusable tooltip element
    const tooltip = document.createElement("div");
    tooltip.id = "glossary-tooltip";
    document.body.appendChild(tooltip);

    fetch(glossaryUrl)
        .then((res) => res.json())
        .then((glossary) => {
            const links = document.querySelectorAll("a[href*='#']");
            links.forEach((link) => {
                const hash = link.getAttribute("href").split("#")[1];
                if (!hash) return;
                const slug = hash.toLowerCase().replace(/[^\w]+/g, "-").replace(/(^-|-$)/g, "");
                let def = glossary[slug];
                if (!def) return;

                // Strip Markdown and format bullets with real line breaks
                def = def
                    .replace(/\*\*(.*?)\*\*/g, '$1')         // bold
                    .replace(/\*(.*?)\*/g, '$1')             // italic
                    .replace(/\[(.*?)\]\(.*?\)/g, '$1')      // links
                    .replace(/`([^`]+)`/g, '$1')             // inline code
                    .replace(/#+\s/g, '')                    // headers
                    .replace(/>\s*/g, '')                    // blockquotes
                    .replace(/-\s+/g, '• ')                  // markdown list → bullet
                    .replace(/•\s*/g, '\n• ')                // line breaks before bullets
                    .trim();

                // Attach event listeners
                link.classList.add(tooltipClass);
                link.addEventListener("mouseenter", (e) => {
                    tooltip.innerHTML = def.replace(/\n/g, '<br>');
                    tooltip.style.display = "block";
                    const rect = link.getBoundingClientRect();
                    tooltip.style.top = `${rect.top + window.scrollY - tooltip.offsetHeight - 10}px`;
                    tooltip.style.left = `${rect.left + window.scrollX}px`;
                });

                link.addEventListener("mouseleave", () => {
                    tooltip.style.display = "none";
                });
            });
        });

    injectStyles();

    function injectStyles() {
        const style = document.createElement("style");
        style.textContent = `
      #glossary-tooltip {
        display: none;
        position: absolute;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 10px 12px;
        font-size: 0.68rem;
        line-height: 1.5;
        max-width: 320px;
        white-space: pre-line;
        border-radius: 6px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        z-index: 1000;
        pointer-events: none;
      }

      .${tooltipClass} {
        cursor: help;
      }
    `;
        document.head.appendChild(style);
    }
});