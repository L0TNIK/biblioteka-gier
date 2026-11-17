
// ============================================================
// USTAWIENIA I ELEMENTY STRONY
// ============================================================
const API = "http://127.0.0.1:8000";

function token() {
    return localStorage.getItem("token");
}

async function apiFetch(sciezka, opcje = {}) {
    const odp = await fetch(`${API}${sciezka}`, {
        ...opcje,
        headers: { ...(opcje.headers || {}), "Authorization": `Bearer ${token()}` },
    });
    if (odp.status === 401 || odp.status === 403) {
        localStorage.removeItem("token");
        window.location.href = "logowanie.html";
    }
    return odp;
}

if (!token()) {
    window.location.href = "logowanie.html";
}

// lista gier, wyszukiwanie i sortowanie
const lista = document.getElementById("games-list");
const poleSzukaj = document.getElementById("search");
const przyciskSzukaj = document.getElementById("search-button");
const sortowanie = document.getElementById("sort");
const filtrGatunku = document.getElementById("genre-filter");

// okienko dodawania
const modalDodaj = document.getElementById("add-game-modal");
const poleNazwa = document.getElementById("game-name");
const wynikiSteam = document.getElementById("steam-results");
const poleOcena = document.getElementById("game-rating");
const poleGatunek = document.getElementById("game-genre");

// okienko edycji
const modalEdytuj = document.getElementById("edit-game-modal");
const poleEdytujGatunek = document.getElementById("edit-game-genre");

// okienko usuwania
const modalUsun = document.getElementById("delete-game-modal");

// ============================================================
// POMOCNICZE: OKIENKA (MODALE)
// ============================================================
function pokazModal(modal) {
    modal.style.display = "flex";
}

function ukryjModal(modal) {
    modal.style.display = "none";
}

// Kliknięcie w ciemne tło (poza okienkiem) zamyka okienko.
function zamykajPrzyKlikniecieWTlo(modal, poZamknieciu) {
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            ukryjModal(modal);
            if (poZamknieciu) poZamknieciu();
        }
    });
}


// ============================================================
// LISTA GIER
// ============================================================
async function wczytajGry() {
   
    try {
        const odpowiedz = await apiFetch(
            `/gry?search=${encodeURIComponent(poleSzukaj.value)}&sort=${sortowanie.value}`
        );

        if (!odpowiedz.ok) return;

        const gry = await odpowiedz.json();

        let przefiltrowaneGry = gry;

        if (filtrGatunku.value !== "") {
            przefiltrowaneGry = gry.filter(gra =>
                gra.gatunek === filtrGatunku.value
            );
        }

        lista.innerHTML = "";

        for (const gra of przefiltrowaneGry) {
            lista.appendChild(stworzKarte(gra));
        }
    }
    catch (blad) {
        console.error(blad);
        lista.textContent = "Nie mozna polaczyc sie z serwerem";
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
    const opis = document.createElement("p");
    opis.className = "game-description";
    const mojaOcena = document.createElement("p");
    mojaOcena.className = "game-rating";
    if (gra.ocena) {
        let klasaOceny = "ocena-srednia";
        if (gra.ocena >= 8) klasaOceny = "ocena-wysoka";
        else if (gra.ocena <= 4) klasaOceny = "ocena-niska";

        mojaOcena.innerHTML = `Moja ocena: <span class="ocena-wartosc ${klasaOceny}">${gra.ocena}/10</span>`;
    } else {
        mojaOcena.innerHTML = `<span class="brak-danych">Brak oceny</span>`;
    }

    const gatunek = document.createElement("p");
    gatunek.className = "game-genre";
    if (gra.gatunek) {
        gatunek.innerHTML = `Gatunek: <span class="gatunek-tag">${gra.gatunek}</span>`;
    } else {
        gatunek.innerHTML = `<span class="brak-danych">Brak gatunku</span>`;
    }

    info.append(tytul, opis, mojaOcena, gatunek);

    const akcje = document.createElement("div");
    akcje.className = "game-actions";
    const edytuj = document.createElement("button");
    edytuj.textContent = "Edytuj";
    edytuj.addEventListener("click", () => edytujGre(gra));

    const usun = document.createElement("button");
    usun.textContent = "Usuń grę";
    usun.addEventListener("click", () => usunGre(gra.id));
    akcje.append(edytuj, usun);

    karta.append(obraz, info, akcje);

    if (gra.steam_appid) {
        wczytajOpis(gra.steam_appid, opis);
    }
    return karta;
}

async function wczytajOpis(appId, opisEl) {
    try {
        const odp = await fetch(`${API}/steam/details/${appId}`);
        if (!odp.ok) throw new Error("blad");
        const dane = await odp.json();
        opisEl.textContent = dane.opis || "";
    } catch (blad) {
        console.error("Opis ze Steama:", blad);
    }
}

// ============================================================
// WYSZUKIWANIE I SORTOWANIE
// ============================================================
przyciskSzukaj.addEventListener("click", wczytajGry);
poleSzukaj.addEventListener("keydown", (e) => {
    if (e.key === "Enter") wczytajGry();
});
sortowanie.addEventListener("change", wczytajGry);
filtrGatunku.addEventListener("change", wczytajGry);


// ============================================================
// DODAWANIE GIER
// ============================================================
let wybranaGra = null;   // gra wybrana ze Steama; null = własna gra

document.getElementById("open-add-game").addEventListener("click", () => {
    poleNazwa.value = "";
    poleOcena.value = "";
    poleGatunek.value = "";
    wynikiSteam.innerHTML = "";
    wybranaGra = null;
    pokazModal(modalDodaj);
});

document.getElementById("cancel-add-game").addEventListener("click", () => {
    ukryjModal(modalDodaj);
});

zamykajPrzyKlikniecieWTlo(modalDodaj);

async function szukajWSteamie() {
    const fraza = poleNazwa.value.trim();
    if (!fraza) return;

    wybranaGra = null;
    wynikiSteam.textContent = "Szukam...";
    try {
        const odp = await fetch(`${API}/steam/search?term=${encodeURIComponent(fraza)}`);
        if (!odp.ok) throw new Error("blad");
        const wyniki = await odp.json();

        wynikiSteam.innerHTML = "";

        if (!wyniki || wyniki.length === 0) {
            wynikiSteam.innerHTML = '<div class="no-results">Nie dodano gry</div>';
            return;
        }

        for (const gra of wyniki) {
            const wiersz = document.createElement("div");
            wiersz.className = "wynik";
            wiersz.textContent = gra.tytul;
            wiersz.addEventListener("click", () => {
                wybranaGra = gra;
                poleNazwa.value = gra.tytul;
                for (const w of wynikiSteam.children) w.classList.remove("wybrany");
                wiersz.classList.add("wybrany");
            });
            wynikiSteam.appendChild(wiersz);
        }
    } catch (blad) {
        wynikiSteam.textContent = "Steam nie odpowiada. Możesz dodać grę, wpisując samą nazwę.";
    }
}

async function dodajGre() {
    const tytul = poleNazwa.value.trim();
    if (!tytul) return;

    let ocena = null;
    if (poleOcena.value.trim() !== "") {
        ocena = Number(poleOcena.value);
        if (!Number.isInteger(ocena) || ocena < 1 || ocena > 10) {
            alert("Ocena musi być liczbą całkowitą od 1 do 10.");
            return;
        }
    }

    const dane = {
        tytul: tytul,
        ocena: ocena,
        gatunek: poleGatunek.value
    };

    if (wybranaGra) {
        dane.steam_appid = wybranaGra.steam_appid;
        dane.image = wybranaGra.image;
    }

    const odp = await apiFetch("/gry", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dane),
    });
    if (!odp.ok) {
        alert("Nie udało się dodać gry.");
        return;
    }
    ukryjModal(modalDodaj);
    wczytajGry();
}

document.getElementById("search-steam").addEventListener("click", szukajWSteamie);
poleNazwa.addEventListener("keydown", (e) => {
    if (e.key === "Enter") szukajWSteamie();
});
poleNazwa.addEventListener("input", () => {
    wybranaGra = null;
});
document.getElementById("confirm-add-game").addEventListener("click", dodajGre);


// ============================================================
// EDYCJA GIER
// ============================================================
let graDoEdycji = null;

function edytujGre(gra) {
    graDoEdycji = gra;
    poleEdytujGatunek.value = gra.gatunek || "";
    pokazModal(modalEdytuj);
}

async function zapiszEdycje() {
    if (graDoEdycji === null) return;

    const dane = {
        tytul: graDoEdycji.tytul,
        ocena: graDoEdycji.ocena,
        gatunek: poleEdytujGatunek.value || null,
    };

    const odp = await apiFetch(`/gry/${graDoEdycji.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dane),
    });
    if (!odp.ok) {
        alert("Nie udało się zapisać zmian.");
        return;
    }
    ukryjModal(modalEdytuj);
    graDoEdycji = null;
    wczytajGry();
}

document.getElementById("cancel-edit-game").addEventListener("click", () => {
    ukryjModal(modalEdytuj);
    graDoEdycji = null;
});

document.getElementById("confirm-edit-game").addEventListener("click", zapiszEdycje);

zamykajPrzyKlikniecieWTlo(modalEdytuj, () => {
    graDoEdycji = null;
});


// ============================================================
// USUWANIE GIER
// ============================================================
let graDoUsuniecia = null;

function usunGre(id) {
    graDoUsuniecia = id;
    pokazModal(modalUsun);
}

document.getElementById("cancel-delete-game").addEventListener("click", () => {
    ukryjModal(modalUsun);
    graDoUsuniecia = null;
});

document.getElementById("confirm-delete-game").addEventListener("click", async () => {
    if (graDoUsuniecia === null) return;

    const odp = await apiFetch(`/gry/${graDoUsuniecia}`, { method: "DELETE" });
    if (!odp.ok) alert("Nie udało się usunąć gry.");

    ukryjModal(modalUsun);
    graDoUsuniecia = null;
    wczytajGry();
});

zamykajPrzyKlikniecieWTlo(modalUsun, () => {
    graDoUsuniecia = null;
});

document.getElementById("logout").addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "logowanie.html";
});

// ============================================================
// START
// ============================================================
wczytajGry();
