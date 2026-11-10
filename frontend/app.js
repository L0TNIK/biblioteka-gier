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
    info.appendChild(tytul);

    const akcje = document.createElement("div");
    akcje.className = "game-actions";

    //-------------------------------------------------------------

    const edytuj = document.createElement("button");
    edytuj.textContent = "Edytuj";

    edytuj.addEventListener("click", () => {
    document.getElementById("edit-game-modal").style.display = "flex";
    });
    //------------------------------------------------------------
    const usun = document.createElement("button");
    usun.textContent = "Usuń grę";
    usun.addEventListener("click", () => usunGre(gra.id));
    akcje.append(edytuj, usun);

    karta.append(obraz, info, akcje);
    return karta;
}

let graDoUsuniecia = null;

function usunGre(id) {
    graDoUsuniecia = id;

    document.getElementById("delete-game-modal").style.display = "flex";
}

przyciskSzukaj.addEventListener("click", wczytajGry);
poleSzukaj.addEventListener("keydown", (e) => {
    if (e.key === "Enter") wczytajGry();
});
sortowanie.addEventListener("change", wczytajGry);

const TLUMACZENIA = {
    "Overwhelmingly Positive": "Przytłaczająco pozytywne",
    "Very Positive": "Bardzo pozytywne",
    "Positive": "Pozytywne",
    "Mostly Positive": "W większości pozytywne",
    "Mixed": "Mieszane",
    "Mostly Negative": "W większości negatywne",
    "Negative": "Negatywne",
    "Very Negative": "Bardzo negatywne",
    "Overwhelmingly Negative": "Przytłaczająco negatywne",
};

//----------------------------------------------------------------------------
// DODAWANIE GIER
//----------------------------------------------------------------------------
const modalDodaj = document.getElementById("add-game-modal");
const poleNazwa = document.getElementById("game-name");
const wynikiSteam = document.getElementById("steam-results");

let wybranaGra = null;   // gra wybrana ze Steama; null = własna gra

document.getElementById("open-add-game").addEventListener("click", () => {
    poleNazwa.value = "";
    wynikiSteam.innerHTML = "";
    wybranaGra = null;
    modalDodaj.style.display = "flex";
});

document.getElementById("cancel-add-game").addEventListener("click", () => {
    modalDodaj.style.display = "none";
});

modalDodaj.addEventListener("click", (e) => {
    if (e.target === modalDodaj) modalDodaj.style.display = "none";
});

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

    const dane = { tytul: tytul };
    if (wybranaGra) {
        dane.steam_appid = wybranaGra.steam_appid;
        dane.image = wybranaGra.image;
    }

    await fetch(`${API}/gry`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dane),
    });
    modalDodaj.style.display = "none";
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



//-----------------------------------------------------------------------------------

const editModal = document.getElementById("edit-game-modal");

document.getElementById("cancel-edit-game").addEventListener("click", () => {
    editModal.style.display = "none";
});

editModal.addEventListener("click", (e) => {
    if (e.target === editModal) {
        editModal.style.display = "none";
    }
});




const deleteModal = document.getElementById("delete-game-modal");

document.getElementById("cancel-delete-game").addEventListener("click", () => {
    deleteModal.style.display = "none";
    graDoUsuniecia = null;
});

document.getElementById("confirm-delete-game").addEventListener("click", async () => {
    if (graDoUsuniecia === null) return;

    await fetch(`${API}/gry/${graDoUsuniecia}`, {
        method: "DELETE"
    });

    deleteModal.style.display = "none";
    graDoUsuniecia = null;

    wczytajGry();
});

deleteModal.addEventListener("click", (e) => {
    if (e.target === deleteModal) {
        deleteModal.style.display = "none";
        graDoUsuniecia = null;
    }
});



//----------------------------------------------------------------------------
wczytajGry();