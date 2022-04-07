setTimeout(function () {
    get_performance();
}, 4000);

function get_performance() {
    table = document.getElementsByTagName('table')[0]
    tbody = table.getElementsByTagName('tbody')[0]
    tbody__trs = tbody.getElementsByTagName('tr')

    for (tbody__tr_index = 0; tbody__tr_index < tbody__trs.length; tbody__tr_index++) {
        tbody__tr = tbody__trs[tbody__tr_index]
        tbody__tds = tbody__tr.getElementsByTagName('td')

        let apdex = tbody__tds[9]   // 改列的数值改为 @ 的开发
        apdex.innerText = ''
        transaction = tbody__tds[1]  // 请求的 url
        let users = tbody__tds[10]   // 改列的数值改为 @ 的开发
        method = tbody__tds[4]  // 请求的 url

        if (transaction.innerText == '/1/{version}/labors/{pk}/identity4/' && method == 'POST') {
            apdex.innerText = '[网络请求] 四要素认证'
            console.log(method.innerText)
        }
        if (transaction.innerText == '/1/companylabors/contract_download/') {
            apdex.innerText = '@王旭阳'
            users.innerText = 'https://redmine.iqusong.com/issues/7634'
        }
    }

}
