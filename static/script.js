const startups = [
  {
    nome: "Turbi",
    resumo: "Startup de aluguel de carros 100% digital que permite alugar um carro por algumas horas, dias ou meses, através de uma aplicação.",
    imagem: "img/turbi.png",
    link: "https://www.turbi.com.br"
  },
  {
    nome: "Vammo",
    resumo: "Startup brasileira de mobilidade elétrica que oferece aluguel de motos elétricas para motoboys e entregadores de aplicativos.",
    imagem: "img/vammo.png",
    link: "https://vammo.com/"
  },
  {
    nome: "IGrenn",
    resumo: "Startup que se dedica a fornecer soluções de energia solar para redução de custos na conta de luz, sem exigir investimentos em instalação de placas solares.",
    imagem: "img/igreen.png",
    link: "https://www.igreenenergy.com.br/"
  },
  {
    nome: "Blip",
    resumo: "Crie boas conversas em qualquer canal com a melhor plataforma de IA para atendimento automatizado.",
    imagem: "img/blip.jpeg",
    link: "https://www.digital.blip.ai/"
  },
  {
    nome: "Financeiramente",
    resumo: "Conecta sua mente as finanças e te tira do Vermelho.",
    imagem: "img/FinanceiraMente.png",
    link: "https://www.joblink.com"
  },
  {
    nome: "NotCo",
    resumo: "Quando descobrimos que havia uma maneira de deixar a comida que amamos ainda melhor, não perguntamos por quê, dissemos Why Not.",
    imagem: "img/notco.png",
    link: "https://notco.com/br/"
  },
  {
    nome: "",
    resumo: "Wearables",
    imagem: "img/",
    link: "https://"
  },
  {
    nome: "",
    resumo: "Blockchain.",
    imagem: "img/",
    link: "https://"
  },
  {
    nome: "",
    resumo: "Drones ",
    imagem: "img/",
    link: "https://"
  }
];

let currentIndex = 0;
const cardsPerView = 3;
const cardContainer = document.getElementById("card-container");

function renderCards() {
  cardContainer.style.opacity = 0;
  setTimeout(() => {
    cardContainer.innerHTML = "";
    const slice = startups.slice(currentIndex, currentIndex + cardsPerView);
    slice.forEach((startup) => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        ${startup.imagem ? `<img src="${startup.imagem}" alt="${startup.nome}" class="card-img"/>` : ""}
        <strong>${startup.nome}</strong><br/>
        <small>${startup.resumo}</small><br/><br/>
        <button class="card-btn" onclick="window.open('${startup.link}', '_blank')">Visitar site</button>
      `;
      cardContainer.appendChild(div);
    });
    cardContainer.style.opacity = 1;
  }, 200);
}

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

document.addEventListener("DOMContentLoaded", renderCards);

