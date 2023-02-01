setTimeout(function () {
    run();
}, 1000);

function run() {
    setInterval(function () {
        names = document.getElementsByClassName('basicInfo-item name')
        for (index = 0; index < names.length; index++) {
            name = names[index].innerHTML
            console.log('name:' + name)
            if (name == '发行日期') {
                release_time = names[index].nextElementSibling.textContent.split("\n")[1]
                release_time = release_time.split('年')[0]
            }
            if (name == '歌曲原唱') {
                singer = names[index].nextElementSibling.children[0].innerHTML
            }
            if (name == '所属专辑') {
                album = names[index].nextElementSibling.children[0].innerHTML
            }
            if (name == '中文名') {
                song = names[index].nextElementSibling.innerHTML.replace('\n', '')
                // names[index].select()
            }
        }
        value = '[' + release_time + '][' + singer + '][' + album + '][' + song + '].mp4'
        document.getElementById('query').value = value
    }, 1000)

}
