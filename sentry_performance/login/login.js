setTimeout(function () {
    get_performance();
}, 2000);

function get_performance() {
    let table = document.getElementsByTagName('table')[0]
    let tbody = table.getElementsByTagName('tbody')[0]
    let tbody__trs = tbody.getElementsByTagName('tr')
    for (i = 0; i < tbody__trs.length; i++) {
        let tbody__tr = tbody__trs[i]
        console.log(tbody__tr)
    }

}
