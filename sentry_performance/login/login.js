setTimeout(function () {
    get_performance();
}, 4000);

function get_performance() {

    // 过滤掉不想看的
    // !transaction:v1.tasks* !transaction:v1.celery_tasks.* !transaction:/aihbvnrugblnjgen*


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
        if (transaction == '/1/{version}/laborbankaccount/{pk}/' && method == 'PUT') {
            apdex.innerText = '[网络请求] 三要素认证'
        }
        if (transaction == '/1/labors/{pk}/mobile/' && method == 'POST') {
            apdex.innerText = '陈海鸥'
        }
        if (transaction == '/1/localwallettransaction/' && method == 'GET') {
            apdex.innerText = '统计所有的数据，全盘扫描，比较耗时'
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
        if (transaction == '/1/companylabors/update_status/' && method == 'POST') {
            apdex.innerText = '王旭阳'
            users.innerText = 'https://redmine.iqusong.com/issues/7861'
        }
        if (transaction == '/1/topup_record/' && method == 'GET') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/7897'
        }
        if (transaction == '/1/contract_template/{pk}/' && method == 'PUT') {
            apdex.innerText = '[网络请求] 企业身认证 TODO 根据二期的原型再考虑是否可以用异步'
        }
        if (transaction == '/1/services/two_detection/' && method == 'GET') {
            apdex.innerText = '[网络请求] 二要素认证'
        }
        if (transaction == '/openapi/{version}/agency/labors/' && method == 'POST') {
            apdex.innerText = '[网络请求] 二要素认证'
        }
        if (transaction == '/1/agencies/{pk}/zhaoshang/' && method == 'GET') {
            apdex.innerText = '[网络请求] 招商银行'
        }
        if (transaction == '/1/{version}/requirement_agency/labor_ids/' && method == 'GET') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/7962'
        }
        if (transaction == '/1/labors/{pk}/get_public_account_list/' && method == 'GET') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/7966'
        }
        if (transaction == '/1/{version}/labor_cdl/{pk}/wallet/' && method == 'GET') {
            apdex.innerText = '[网络请求] 钱包服务'
        }
        if (transaction == '/1/agencies/account_confirmation/' && method == 'GET') {
            apdex.innerText = '[网络请求] 钱包服务'
        }
        if (transaction == '/1/labors/wallet_transactions/' && method == 'GET') {
            apdex.innerText = '[网络请求] 钱包服务'
        }
        if (transaction == '/1/{version}/labor_lls/{pk}/wallet/' && method == 'GET') {
            apdex.innerText = '[网络请求] 钱包服务'
        }
        if (transaction == '/1/agencies_four/{pk}/' && method == 'PUT') {
            apdex.innerText = '王旭阳'
            users.innerText = 'https://redmine.iqusong.com/issues/7985'
        }
        if (transaction == '/1/companylabors/template_download/' && method == 'GET') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/8170'
        }
        if (transaction == '/1/requirement_agency_list/' && method == 'GET') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/8001'
        }
        if (transaction == '/1/roles/' && method == 'POST') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/8056'
        }
        if (transaction == '/1/{version}/wx_authorization_api/web_access_token/' && method == 'GET') {
            apdex.innerText = '[网络请求] 微信接口'
        }
        if (transaction == '/1/weixin/wx_bind_url2/' && method == 'GET') {
            apdex.innerText = '[网络请求] 微信'
        }
        if (transaction == '/1/contracts/{pk}/sign/' && method == 'GET') {
            apdex.innerText = '[网络请求] 获得合同服务的链接'
        }
        if (transaction == '/1/usersaas/' && method == 'GET') {
            apdex.innerText = '[网络请求] 钱包服务'
        }
        if (transaction == '/1/weixin/redirect/' && method == 'GET') {
            apdex.innerText = '[网络请求] 微信接口'
        }
        if (transaction == '/1/weixin/wx_login/' && method == 'POST') {
            apdex.innerText = '[网络请求] 微信接口'
        }
        if (transaction == '/openapi/{version}/econtracts/plus_create_contract/' && method == 'POST') {
            apdex.innerText = '[网络请求] 合同接口'
        }
        if (transaction == '/1/companylabors/tax_registration_file_download_serverless/' && method == 'GET') {
            apdex.innerText = '李帅华'
            users.innerText = 'https://redmine.iqusong.com/issues/8157'
        }
        if (transaction == '/1/settlements/get_list_sum/' && method == 'GET') {
            apdex.innerText = '王旭阳'
            users.innerText = 'https://redmine.iqusong.com/issues/8156'
        }
        if (transaction == '/1/stop_records' && method == 'GET') {
            apdex.innerText = '李帅华'
            users.innerText = 'https://redmine.iqusong.com/issues/8155'
        }
        if (transaction == '/1/screen_deal_amount_data/get_data_count/' && method == 'GET') {
            apdex.innerText = '前端正在优化'
            users.innerText = 'https://redmine.iqusong.com/issues/8160'
        }
        if (transaction == '/1/weixin/wx_bind_url1/' && method == 'GET') {
            apdex.innerText = '[网络请求] parse 接口'
        }
        if (transaction == '/1/weixin/wx_bind_url2/' && method == 'GET') {
            apdex.innerText = '[网络请求] parse 接口'
        }
        if (transaction == '/openapi/{version}/econtracts/plus_create_contract/' && method == 'POST') {
            apdex.innerText = '[网络请求] 合同服务'
        }
    }
}
