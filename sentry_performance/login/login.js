setTimeout(function () {
    get_performance();
}, 4000);

function get_performance() {

    if (location.pathname.startsWith("/organizations/zhongjian/performance/lls_api:")) {
        console.log('Performance -> Transaction Summary -> Event Details')

        // 根据 X-Request-Id 找到用户
        setInterval(function () {
            tds = document.getElementsByClassName('key css-1y4sfnd e7hu3jh0')
            for (td_index = 0; td_index < tds.length; td_index++) {
                td_html = tds[td_index].innerHTML
                if (td_html == 'X-Request-Id') {
                    x_request_id = tds[td_index].nextElementSibling
                    console.log('x_request_id' + ':' + x_request_id.textContent)
                    const http = new easyHTTP;
                    const data = {
                        href: location.pathname,
                    };
                    if (!x_request_id.textContent.includes('(用户:')) {
                        http.get(
                            'http://127.0.0.1:8000/v4/sentry/user?X-Request-Id=' + encodeURIComponent(x_request_id.textContent),
                            data, function (status, responseText) {
                                console.log(new Date() + ' 请求返回: ' + responseText)
                                if (!x_request_id.textContent.includes('(用户:')) {
                                    x_request_id_span = x_request_id.children[0].children[0]
                                    x_request_id_span.innerText = x_request_id_span.innerText + '(用户:' + responseText + ')'
                                }
                            }
                        );
                    } else {
                        console.log('有用户啊     ')
                    }

                }
            }
        }, 1000)

    }

    // 过滤掉不想看的
    // !transaction:v1.tasks* !transaction:v1.celery_tasks.* !transaction:/aihbvnrugblnjgen*

    // 为定位到的代码的位置添加链接
    setInterval(function () {

        // 找到所有 Operation 的描述内容
        spans = document.getElementsByClassName('val-string')

        for (span_index = 0; span_index < spans.length; span_index++) {
            span_inner_html = spans[span_index].innerHTML

            // 如果描述的内容已经添加链接，不再操作
            if (span_inner_html.indexOf('href') == -1) {

                // 内容中存在 db at File 或者 http at File，说明是有具体代码位置的内容
                if (span_inner_html.indexOf(' at File "') != -1) {

                    // 获得文件路径
                    replace_str = span_inner_html.substring(span_inner_html.indexOf('"') + 1, span_inner_html.indexOf('",'))
                    // 获得执行的代码在第几行
                    line = span_inner_html.substring(span_inner_html.indexOf(', line ') + 7, span_inner_html.indexOf(', in '))
                    // 获得代码的版本号
                    release = document.getElementsByClassName('css-1xdhyk6 eqmhduc3')[0].innerHTML
                    // 拼接出可以精确定位到所在代码行的 gitlab 链接，
                    href = 'https://gitlab.iqusong.com/llsaas/api/-/blob/release-' + release + '/' + replace_str + '#L' + line
                    // 将文件路径替换成带链接的文件名
                    replace_to = '<a href="' + href + '" target="_blank" >' + replace_str + '</a>'
                    spans[span_index].innerHTML = span_inner_html.replace(replace_str, replace_to)
                }
            }
        }
    }, 1000)

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
        users.innerText = ''
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
            users.innerText = 'https://redmine.iqusong.com/issues/8439'
        }
        if (transaction == '/1/contract_template/{pk}/' && method == 'PUT') {
            apdex.innerText = '[网络请求] 企业身认证 TODO 根据二期的原型再考虑是否可以用异步'
        }
        if (transaction == '/1/services/two_detection/' && method == 'GET') {
            apdex.innerText = '[网络请求] 二要素认证'
        }
        if (transaction == '/1/services/ic/' && method == 'GET') {
            apdex.innerText = '[网络请求] 天眼查'
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
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/8453'
        }
        if (transaction == '/1/screen_deal_amount_data/get_data_count/' && method == 'GET') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/8438'
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
        if (transaction == '/1/offline/identity3/' && method == 'POST') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/8212'
        }
        if (transaction == '/1/companylabors/update_stop_status/' && method == 'POST') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/8210'
        }
        if (transaction == '/1/{version}/parks/saas_index_data_statistics/' && method == 'GET') {
            apdex.innerText = '陈海鸥'
            users.innerText = 'https://redmine.iqusong.com/issues/8483'
        }
        if (transaction == '/1/settlements/{pk}/settle/' && method == 'POST') {
            apdex.innerText = '[网络请求] 招商银行'
        }
        if (transaction == '/1/companies/cmbpay_prepay_to_card/' && method == 'POST') {
            apdex.innerText = '[网络请求] 招商银行'
        }
        if (transaction == '/1/businesspromotionfee/bpf_cdl/' && method == 'PUT') {
            apdex.innerText = '[网络请求] cdl 获得业务推广费'
        }
        if (transaction == '/1/companies/{pk}/enterprise_identity/' && method == 'POST') {
            apdex.innerText = '[网络请求] 合同服务 获得企业认证地址'
        }
        if (transaction == '/1/users/sms_agency_offline_settle/' && method == 'POST') {
            apdex.innerText = '[网络请求] 短信服务'
        }
        if (transaction == '/1/common/tencent_h5_face_redirect/' && method == 'GET') {
            apdex.innerText = '[网络请求] 腾讯人脸识别结果'
        }
        if (transaction == '/1/{version}/labors/facial_identification_rule/' && method == 'GET') {
            apdex.innerText = '[网络请求] 腾讯人脸识别申请请求'
        }
        if (transaction == '/1/companies/{pk}/enterprise_identity_notify/' && method == 'GET') {
            apdex.innerText = '[网络请求] 合同服务'
        }
        if (transaction == '/1/{version}/companies/{pk}/update_company_contract_info/' && method == 'GET') {
            apdex.innerText = '[网络请求] 二要素认证'
        }
        if (transaction == '/1/{version}/companies/{pk}/add_base_info/' && method == 'PUT') {
            apdex.innerText = '[网络请求] OSS'
        }
        if (transaction == '/1/{version}/companies/' && method == 'POST') {
            apdex.innerText = '[网络请求] OSS'
        }
        if (transaction == '/1/contracts/' && method == 'GET') {
            apdex.innerText = '[网络请求] 合同服务'
        }
        if (transaction == '/1/{version}/labors/certification4thirdparty_result/' && method == 'GET') {
            apdex.innerText = '[网络请求] 福建税务'
        }
        if (transaction == '/1/labors/{pk}/get_wxpay_income/' && method == 'GET') {
            apdex.innerText = '[网络请求] 微信支付查询'
        }
    }
}
