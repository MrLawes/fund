setTimeout(function () {
    run();
}, 1000);

function run() {
    setInterval(function () {
        caption = document.getElementsByClassName('caption')[0]
        song = caption.children[0]
        if (!song.innerHTML.includes('href')) {
            href = "https://www.baidu.com/s?wd=" + encodeURIComponent(song.innerHTML)
            song.innerHTML = '<a href="' + href + '" target="_blank">' + song.innerHTML + '</a>'
            console.log(song + ':song')
        }
    }, 1000)
}
