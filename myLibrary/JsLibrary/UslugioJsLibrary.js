
function show_more() {
    var conteiner = $('#loadmore-btn-conteiner').attr('style');
    if (conteiner == "display: none;"){
        return 0;
    }

    var el = $('.btn.btn-default.btn-lg.btn-block.loadmore');
    if (el.length == 0) {
        return false;
    }

    el.click()
    return 1;
}

function count_items(){
    var el = $('.items_n');
    if (el.length == 0) {
        return false;
    }

    return $('.items_n').length
}

function open_item(index) {
    var el = $('.items_n').eq(index).find('.title.showone');
    if (el.length == 0) {
        return false;
    }

    el.click()
    return true;
}

function get_phone() {
    var el = $('.showphone1.btn.btn-primary.btn-lg.btn-block');
    if (el.length == 0) {
        return false;
    }
    $('.post_text_more').click();
    el.focus();
    el.click();

    text = el.text();
    if (text == "загрузка.."){
        return false;
    }

    return text;
}

function back() {
    var el = $('.btn.btn-default.btn-lg.one-post-item-back');
    if (el.length == 0) {
        return false;
    }

    el.click()
    return true;
}

function scroll_phone(){
    var el = $('.showphone1.btn.btn-primary.btn-lg.btn-block');
    if (el.length == 0) {
        return false;
    }

    $('html').scrollTop(el.offset().top-20);
    return true;
}

function scroll_item(index){
    var el = $('.items_n').eq(index).find('.title.showone');
    if (el.length == 0) {
        return false;
    }

    $('html').scrollTop(el.offset().top-20);
    return true;
}

function name(){
    var el = $('.show_one_btns').eq(0).find('b');
    if (el.length == 0) {
        return false;
    }

    var str = el.text();
    var data = "None";
    if (str.match(/[^\s]+/)){
        data = str.match(/[^\s]+/)[0];
    }
    return data;
}

function name_and_service(){
    var el = $('.items_n');
    if (el.length == 0) {
        return false;
    }

    var title = el.find(".title.showone");
    var name = [];
    var service = [];
    var data = []
    for (var i = 0; i < title.length; i++) {

        data = title.eq(i).text();
        data = data.replace(/\s+/ig, " ")
        data = data.replace(/^\s+|\s+$/ig, "")
        data = data.split(": ")
        if (data.length == 2 && data[0].length > 1){
            name.push(data[0]);
            service.push(data[1]);
        }
        else if(data.length == 2){
            name.push("None");
            service.push(data[1]);
        }
        else{
            name.push("None");
            service.push(data[0]);
        }

    }
    return [name, service];
}
