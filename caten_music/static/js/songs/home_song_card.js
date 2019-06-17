// static/js/home_song_card.js

var colorCollection = [
    "#ff7675",
    "#ffab6e",
    "#e0d090",
    "#00c894",
    "#64b9ff",
    "#0974e3",
    "#b29bfe",
]

var colorCollection2 = [
    "#FFD74D",
    "#FFB13B",
    "#FFC23A",
    "#FFD03B",
    "#FFD050",
    "#FFE03D",
]

setTimeout(function(){
    for (let i = 0; i < 6; i++) {
        let selectName = "#song-card-id-" + String(i)
        $(selectName).css("background-color", colorCollection2[i])
    }
}, 10)

