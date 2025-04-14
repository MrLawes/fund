setTimeout(function () {
    run();
}, 1000);

function run() {
    setInterval(function () {
        names = document.getElementsByClassName('basicInfoItem_dQpCj itemName_HvzSE')
        release_time = ''
        singer = ''
        album = ''
        song = ''
        for (index = 0; index < names.length; index++) {
            name = names[index].innerHTML
            if (name == '发行日期') {
                release_time = names[index].nextElementSibling.textContent
                release_time = release_time.split('年')[0]
            }
            if (name == '发行时间') {
                release_time = names[index].nextElementSibling.textContent.split("\n")[1]
                release_time = release_time.split('年')[0].split('-')[0].split('.')[0]
            }
            if (name == '专辑歌手') {
                if (names[index].nextElementSibling.children.length == 0) {
                    singer = names[index].nextElementSibling.innerHTML
                } else {
                    singer = names[index].nextElementSibling.children[0].innerHTML
                }
            }
            if (name == '歌曲原唱') {
                if (names[index].nextElementSibling.children.length == 0) {
                    singer = names[index].nextElementSibling.innerHTML
                } else {
                    singer = names[index].nextElementSibling.children[0].innerHTML
                }
                singer = singer.split("</a>")[0]
                singer = singer.split(">")
                singer = singer[singer.length - 1]
            }
            if (name == '所属专辑') {
                if (names[index].nextElementSibling.children.length == 0) {
                    album = names[index].nextElementSibling.innerHTML
                } else {
                    album = names[index].nextElementSibling.children[0].innerHTML
                }
                album = album.replace('》', '').replace('《', '')
            }
            if (name == '中文名') {
                song = names[index].nextElementSibling.innerHTML.replace('\n', '')
                song = song.split('</span>')[0]
                song = song.split('">')
                song = song[song.length - 1]
                song = song.split('<')[0]
            }
        }
        if (album == "") {
            album = song
        }
        value = '[' + release_time + '][' + singer + '][' + album + '][' + song + ']'
        document.getElementsByTagName("input")[0].value = value
    }, 1000)

}
