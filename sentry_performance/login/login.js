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
        transaction = tbody__tds[1].innerText  // 请求的 url
        let users = tbody__tds[10]   // 改列的数值改为 @ 的开发
        method = tbody__tds[4].innerText  // 请求的 url


        if (transaction == '/1/{version}/labors/{pk}/identity4/' && method == 'POST') {
            apdex.innerText = '[网络请求] 四要素认证'
            console.log(method.innerText)
        }
        if (transaction == '/1/companylabors/contract_download/' && method == 'GET') {
            apdex.innerText = '王旭阳'
            users.innerText = 'https://redmine.iqusong.com/issues/7634'
        }
        if (transaction == '/1/{version}/laborbankaccount/{pk}/' && method == 'PUT') {
            apdex.innerText = '[网络请求] 三要素认证'
        }
        if (transaction == '/1/labors/{pk}/mobile/' && method == 'POST') {
            apdex.innerText = '陈海鸥'
        }
        if (transaction == '/1/localwallettransaction/' && method == 'GET') {
            apdex.innerText = '李帅华'
            users.innerText = 'https://redmine.iqusong.com/issues/7801'
        }
        if (transaction == '/1/{version}/companylabors/' && method == 'GET') {
            apdex.innerText = '李帅华'
            users.innerText = 'https://redmine.iqusong.com/issues/7780'
        }
        if (transaction == '/1/{version}/laborbankaccount/' && method == 'POST') {
            apdex.innerText = '[网络请求] 三要素认证'
        }
        if (transaction == '/1/companies/cmbpay_receipt/' && method == 'POST') {
            apdex.innerText = '[网络请求] 访问招商银行接口'
        }
        if (transaction == '/1/companies/cmbpay_to_card/' && method == 'POST') {
            apdex.innerText = '[网络请求] 访问招商银行接口'
        }
        if (transaction == '/1/labors/' && method == 'POST') {
            apdex.innerText = '[网络请求] 二要素认证'
        }
        if (transaction == '/1/labors/not_code_identity3/' && method == 'POST') {
            apdex.innerText = '[网络请求] 三要素认证'
        }
        if (transaction == '/1/{version}/labors/{pk}/update_real_phone/' && method == 'POST') {
            apdex.innerText = '[网络请求] 三要素认证'
        }
        if (transaction == '/1/companylabors/' && method == 'POST') {
            apdex.innerText = '[网络请求] 二要素认证'
        }
        if (transaction == '/1/qr_code_create_labor/create_labor/' && method == 'POST') {
            apdex.innerText = '[网络请求] 二要素认证'
        }
        if (transaction == '/1/labors/sms_verify/' && method == 'POST') {
            apdex.innerText = '[网络请求] 发送短信'
        }
        if (transaction == '/1/offline/sms_verify/' && method == 'POST') {
            apdex.innerText = '[网络请求] 发送短信'
        }
        if (transaction == '/1/companylabors/tax_registration_file_download_serverless/' && method == 'GET') {
            apdex.innerText = '李帅华'
            users.innerText = 'https://redmine.iqusong.com/issues/7815'
        }
        if (transaction == '/1/companies/cmbpay_receipt_fileurl/' && method == 'POST') {
            apdex.innerText = '[网络请求] 招商银行'
        }
        if (transaction == '/1/companylabors/batch_cancel_tax_registration_certificate/' && method == 'POST') {
            apdex.innerText = '李帅华'
            users.innerText = 'https://redmine.iqusong.com/issues/5367'
        }
        if (transaction == '/1/companylabors/upload_tax_registration_certificate/' && method == 'POST') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/7847'
        }
    }
}
