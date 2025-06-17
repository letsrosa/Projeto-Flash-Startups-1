const startups = [
  {
    nome: "Turbi",
    resumo: "Startup de aluguel de carros 100% digital que permite alugar um carro por algumas horas, dias ou meses, através de uma aplicação.",
    imagem: "/static/img/turbi.png",
    link: "https://www.turbi.com.br"
  },
  {
    nome: "Vammo",
    resumo: "Startup brasileira de mobilidade elétrica que oferece aluguel de motos elétricas para motoboys e entregadores de aplicativos.",
    imagem: "/static/img/vammo.png",
    link: "https://vammo.com/"
  }
];

let currentIndex = 0;
const cardsPerView = 3;
const cardContainer = document.getElementById("card-container");

// function renderCards() {
//   cardContainer.style.opacity = 0;
//   setTimeout(() => {
//     cardContainer.innerHTML = "";
//     const slice = startups.slice(currentIndex, currentIndex + cardsPerView);
//     slice.forEach((startup) => {
//       const div = document.createElement("div");
//       div.className = "card";
//       div.innerHTML = `
//         ${startup.imagem ? `<img src="${startup.imagem}" alt="${startup.nome}" class="card-img"/>` : ""}
//         <strong>${startup.nome}</strong><br/>
//         <small>${startup.resumo}</small><br/><br/>
//         <button class="card-btn" onclick="window.open('${startup.link}', '_blank')">Visitar site</button>
//       `;
//       cardContainer.appendChild(div);
//     });
//     cardContainer.style.opacity = 1;
//   }, 200);
// }

function nextSlide() {
  if (currentIndex + cardsPerView < startups.length) {
    currentIndex += cardsPerView;
    renderCards();
  }
}

function prevSlide() {
  if (currentIndex - cardsPerView >= 0) {
    currentIndex -= cardsPerView;
    renderCards();
  }
}

async function carregarIdeias() {
  try {
    const resposta = await fetch('/listar_ideias');
    const ideias = await resposta.json();
    const container = document.getElementById('card-container');
    container.innerHTML = '';

    const todasAsIdeias = [...startups, ...ideias];

    todasAsIdeias.forEach(ideia => {
      const card = document.createElement('div');
      card.classList.add('card');

      card.innerHTML = `
        ${ideia.imagem || ideia.logo ? `<img src="${ideia.imagem || ideia.logo}" alt="Logo da startup" class="card-img"/>` : ''}
        <h3>${ideia.nome || ideia.titulo}</h3>
        <p><strong>Categoria:</strong> ${ideia.categoria || ''}</p>
        <p>${ideia.resumo || ideia.descricao}</p>
        <p><em>Autor: ${ideia.autor || ''}</em></p>
        ${ideia.link ? `<button class="card-btn" onclick="window.open('${ideia.link}', '_blank')">Visitar site</button>` : ''}
      `;

      container.appendChild(card);
    });
  } catch (error) {
    console.error('Erro ao carregar ideias:', error);
  }
}



// Chama automaticamente quando a página carrega
carregarIdeias();


document.addEventListener("DOMContentLoaded", carregarIdeias);

