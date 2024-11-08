const boardElement = document.getElementById('board');
const initialPositions = {
    'a8': '♜', 'b8': '♞', 'c8': '♝', 'd8': '♛', 'e8': '♚', 'f8': '♝', 'g8': '♞', 'h8': '♜',
    'a7': '♟', 'b7': '♟', 'c7': '♟', 'd7': '♟', 'e7': '♟', 'f7': '♟', 'g7': '♟', 'h7': '♟',
    'a1': '♖', 'b1': '♘', 'c1': '♗', 'd1': '♕', 'e1': '♔', 'f1': '♗', 'g1': '♘', 'h1': '♖',
    'a2': '♙', 'b2': '♙', 'c2': '♙', 'd2': '♙', 'e2': '♙', 'f2': '♙', 'g2': '♙', 'h2': '♙'
};

for (let row = 8; row >= 1; row--) {
    for (let col = 0; col < 8; col++) {
        const square = document.createElement('div');
        const coordinate = String.fromCharCode(97 + col) + row;
        square.classList.add('square', (row + col) % 2 === 0 ? 'light' : 'dark');
        square.id = coordinate;
        square.textContent = initialPositions[coordinate] || '';
        square.onclick = () => movePiece(coordinate);
        boardElement.appendChild(square);
    }
}

let selectedPiece = null;
let selectedCoord = null;

function movePiece(coord) {
    const square = document.getElementById(coord);
    const piece = square.textContent;

    if (selectedPiece) {
        document.getElementById(selectedCoord).textContent = '';
        square.textContent = selectedPiece;

        if (['♚', '♖', '♕' ].includes(selectedPiece)) {
            const result = generateChessString();
            document.getElementById('cadena').value = result;
            submitCadena()
        }

        selectedPiece = null;
        selectedCoord = null;
    } else {
        selectedPiece = piece;
        selectedCoord = coord;
    }
}

function generateChessString() {
    const blackPieces = { '♚': 'R', '♛': 'D', '♜': 'T' };
    const whitePieces = { '♔': 'R', '♕': 'D', '♖': 'T', '♗': 'A', '♘': 'C', '♙': 'P' };
    const sections = { king: [], queen: [], rook1: [], rook2: [] };
    let kingPosition = null;
    let queenPosition = null;
    let rookPositions = [];
    
    for (let row = 8; row >= 1; row--) {
        for (let col = 0; col < 8; col++) {
            const coord = String.fromCharCode(97 + col) + row;
            const square = document.getElementById(coord).textContent;

            if (square === '♚') kingPosition = `NR${coord}`;
            if (square === '♛') queenPosition = `ND${coord}`;
            if (square === '♜') rookPositions.push(`NT${coord}`);
        }
    }

    let orderedWhitePieces = [];
    let whiteDame = null;
    let whiteRooks = [];
    let otherPieces = [];

    for (let row = 8; row >= 1; row--) {
        for (let col = 0; col < 8; col++) {
            const coord = String.fromCharCode(97 + col) + row;
            const square = document.getElementById(coord).textContent;

            if (square === '♕') { // Dama
                whiteDame = `BD${coord}`;
            } else if (square === '♖') { // Torres
                whiteRooks.push(`BT${coord}`);
            } else if (Object.keys(whitePieces).includes(square)) { // Otras piezas
                const symbol = whitePieces[square];
                otherPieces.push(`B${symbol}${coord}`);
            }
        }
    }

    if (whiteDame) orderedWhitePieces.push(whiteDame);
    orderedWhitePieces = orderedWhitePieces.concat(whiteRooks);
    orderedWhitePieces = orderedWhitePieces.concat(otherPieces);

    sections.king = [...orderedWhitePieces];
    sections.queen = [...orderedWhitePieces];
    sections.rook1 = [...orderedWhitePieces];
    sections.rook2 = [...orderedWhitePieces];

    let finalString = '';

    if (kingPosition) {
        finalString += kingPosition + '/' + sections.king.join('/');
    }

    if (queenPosition) {
        finalString += '/' + queenPosition + '/' + sections.queen.join('/');
    }

    if (rookPositions[0]) {
        finalString += '/' + rookPositions[0] + '/' + sections.rook1.join('/');
    }

    if (rookPositions[1]) {
        finalString += '/' + rookPositions[1] + '/' + sections.rook2.join('/');
    }

    return finalString;
}

async function submitCadena() {
    const cadena = document.getElementById("cadena").value;
    const formData = new FormData();
    formData.append("cadena", cadena);

    try {
        const response = await fetch("/", {
            method: "POST",
            body: formData
        });
        const data = await response.text();
        document.querySelector(".results").innerHTML = data;
    } catch (error) {
        console.error("Error:", error);
    }
}