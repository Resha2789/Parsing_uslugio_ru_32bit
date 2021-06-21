function get_proxy() {
    var el = $('tbody').eq(0).find('tr');
    if (el.length == 0) {
        return false;
    }
    var array = [];
    var ip = '';
    var port = '';
    for (var i = 0; i < el.length; i++) {
        ip = el.eq(i).find('td').eq(0).text();
        port = el.eq(i).find('td').eq(1).text();

        array.push(ip + ':' + port);
    }
    return array;
}

function get_proxy_from_advanced_name() {
    var el_ip = $('td[data-ip]');
    var el_port = $('td[data-port]');
    var el_sp = $('td[data-ip]').parent();

    if (el_ip.length == 0) {
        return false;
    }

    var array = [];
    var ip = '';
    var port = '';
    var sp = '';
    for (var i = 0; i < el_ip.length; i++) {
        sp = Number(el_sp.eq(i).find('td').eq(5).text())
        if (sp < 1000){
            ip = el_ip.eq(i).text();
            port = el_port.eq(i).text();
            array.push(ip + ':' + port);
        }
    }
    return array;
}