document.addEventListener("DOMContentLoaded", function() {
    const vacancyContainer = document.getElementById("vacancyContainer");
    const paginationControls = document.getElementById("paginationControls");
    const cardsPerPageSelect = document.getElementById("cardsPerPage");

    let currentPage = 1;
    let cardsPerPage = parseInt(cardsPerPageSelect.value);

    function renderVacancies() {
        vacancyContainer.innerHTML = "";
        const start = (currentPage - 1) * cardsPerPage;
        const end = start + cardsPerPage;
        const pageItems = vacancies.slice(start, end);

        pageItems.forEach((vacancy, index) => {
            const article = document.createElement("article");
            article.classList.add("vacancy");
            article.setAttribute("aria-labelledby", `job-title-${start + index + 1}`);

            const header = document.createElement("div");
            header.classList.add("vacancy-header");

            const h3 = document.createElement("h3");
            h3.id = `job-title-${start + index + 1}`;
            h3.textContent = vacancy.job_title;

            header.appendChild(h3);
            article.appendChild(header);

            const section = document.createElement("section");

            const pDesc = document.createElement("p");
            pDesc.textContent = vacancy.job_description;
            section.appendChild(pDesc);

            if (vacancy.job_type) {
                const pType = document.createElement("p");
                pType.innerHTML = `<strong>Service type:</strong> ${vacancy.job_type}`;
                section.appendChild(pType);
            }

            article.appendChild(section);
            vacancyContainer.appendChild(article);
        });

        renderPaginationControls();
    }

    function renderPaginationControls() {
        paginationControls.innerHTML = "";

        const totalPages = Math.ceil(vacancies.length / cardsPerPage);

        if (totalPages <= 1) return;

        const prevBtn = document.createElement("button");
        prevBtn.textContent = "Previous";
        prevBtn.disabled = currentPage === 1;
        prevBtn.addEventListener("click", () => {
            currentPage--;
            renderVacancies();
        });
        paginationControls.appendChild(prevBtn);

        for (let i = 1; i <= totalPages; i++) {
            const pageBtn = document.createElement("button");
            pageBtn.textContent = i;
            pageBtn.disabled = i === currentPage;
            pageBtn.addEventListener("click", () => {
                currentPage = i;
                renderVacancies();
            });
            paginationControls.appendChild(pageBtn);
        }

        const nextBtn = document.createElement("button");
        nextBtn.textContent = "Next";
        nextBtn.disabled = currentPage === totalPages;
        nextBtn.addEventListener("click", () => {
            currentPage++;
            renderVacancies();
        });
        paginationControls.appendChild(nextBtn);
    }

    cardsPerPageSelect.addEventListener("change", () => {
        cardsPerPage = parseInt(cardsPerPageSelect.value);
        currentPage = 1;
        renderVacancies();
    });

    renderVacancies();
});
