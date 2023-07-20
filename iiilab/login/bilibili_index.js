setTimeout(function () {
    run();
}, 1000);

function run() {
    setInterval(function () {
        toolbar_left = document.getElementsByClassName('video-toolbar-left')[0]

        if (toolbar_left.children.length > 4) {
            toolbar_left.removeChild(toolbar_left.lastElementChild);
        }

        if (toolbar_left.children.length <= 4) {

            title = document.getElementsByClassName('video-title')[0].title
            title = title.split('歌曲')[0].split(']')
            if (title.length == 1) {
                title = title[0]
            } else {
                title = title[1]
            }
            title = title.split('】')[0]
            iiilab = document.createElement("a");
            iiilab.href = 'https://bilibili.iiilab.com/?singer=' + title + '&blibliurl=' + location.href
            iiilab.target = '_blank'
            textnode = document.createTextNode("下载");
            iiilab.appendChild(textnode)
            span = document.createElement("span");
            span.appendChild(iiilab);
            toolbar_left.appendChild(span);
            console.log(toolbar_left.children.length)
        }
    }, 1000)
}

