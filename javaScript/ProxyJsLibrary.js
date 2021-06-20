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