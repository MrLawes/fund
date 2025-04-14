setTimeout(function () {
    run();
}, 1000);

function run() {
    setInterval(function () {
        search = location.search.slice(5, location.search.length)
        if (search) {
            input = document.getElementsByTagName('input')[0]
            input.value = location.search.split('blibliurl=')[1]
        }
        caption = document.getElementsByClassName('caption')[0]
        if (caption) {
            song = caption.children[0]
            song_innerHTML = song.innerHTML
            // signer = location.search.split('singer=')[1].split('&')[0]
            // signer = decodeURIComponent(signer)
            // signer = signer.replace('【', '')
            signer = ""
            if (!song_innerHTML.includes('href')) {
                song_innerHTML = song_innerHTML.split('|')[0].split('（')[0]
                href = "https://www.baidu.com/s?wd=" + encodeURIComponent(signer + ' ' + song_innerHTML + ' 百度百科')
                song.innerHTML = '<a href="' + href + '" target="_blank">' + song.innerHTML + '</a>'
            }
        }
    }, 1000)
}
