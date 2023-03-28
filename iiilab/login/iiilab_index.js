setTimeout(function () {
    run();
}, 1000);

function run() {
    setInterval(function () {
        search = location.search.slice(5, location.search.length)
        if (search) {
            input = document.getElementsByTagName('input')[0]
            input.value = location.search.slice(11, location.search.length)
        }
        caption = document.getElementsByClassName('caption')[0]
        if (caption) {
            song = caption.children[0]
            if (!song.innerHTML.includes('href')) {
                href = "https://www.baidu.com/s?wd=" + encodeURIComponent('原唱 ' + song.innerHTML + ' 百科')
                song.innerHTML = '<a href="' + href + '" target="_blank">' + song.innerHTML + '</a>'
            }
        }
    }, 1000)
}
