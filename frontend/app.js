const API = "http://127.0.0.1:8000";

const lista = document.getElementById("games-list");
const poleSzukaj = document.getElementById("search");
const przyciskSzukaj = document.getElementById("search-button");
const sortowanie = document.getElementById("sort");

async function wczytajGry() {
    try {
        const odpowiedz = await fetch(
            `${API}/gry?search=${encodeURIComponent(poleSzukaj.value)}&sort=${sortowanie.value}`
        );
        const gry = await odpowiedz.json();

        lista.innerHTML = "";
        for (const gra of gry) {
            lista.appendChild(stworzKarte(gra));
        }
    }
    catch (blad) {
        console.error(blad);
        lista.textContent = "Nie mozna polaczyc sie z serwerem"
    }
}

function stworzKarte(gra) {
    const karta = document.createElement("article");
    karta.className = "game-card";

    const obraz = document.createElement("div");
    obraz.className = "game-image";
    if (gra.image) {
        const img = document.createElement("img");
        img.src = gra.image;
        obraz.appendChild(img);
    }

    const info = document.createElement("div");
    info.className = "game-info";
    const tytul = document.createElement("h3");
    tytul.textContent = gra.tytul;
    info.appendChild(tytul);

    const akcje = document.createElement("div");
    akcje.className = "game-actions"
    const edytuj = document.createElement("button");
    edytuj.textContent = "Edytuj";
    const usun = document.createElement("button");
    usun.textContent = "Usuń grę";
    usun.addEventListener("click", () => usunGre(gra.id));
    akcje.append(edytuj, usun);

    karta.append(obraz, info, akcje);
    return karta;
}

async function usunGre(id) {
    if (!confirm("Na pewno usunąć tę grę?"))
        return
    await fetch(`${API}/gry/${id}`, { method: "DELETE" });
    wczytajGry();
}

async function pobierzDaneZeSteama(appId) {
    try {
        const odpowiedz = await fetch(`${API}/steam/details/${appId}`);
        
        if (!odpowiedz.ok) {
            throw new Error("Nie znaleziono gry o takim ID na Steam.");
        }

        const dane = await odpowiedz.json();
        
        console.log("Opis:", dane.opis);
        console.log("Ocena Steam:", dane.steam_ocena);
    } catch (blad) {
        console.error("Błąd pobierania ze Steama:", blad);
    }
}

przyciskSzukaj.addEventListener("click", wczytajGry);
poleSzukaj.addEventListener("keydown", (e) => {
    if (e.key === "Enter") wczytajGry();
});

wczytajGry();