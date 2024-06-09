
$(function(){
    $('.post_detail_tr').on('click', function(){
       let post_id = $(this).attr('post_id');
       let view_type = 'detail'
       post_detail_info(post_id, view_type);
    });
    $("#post_cont").on("summernote.enter", function(we, e) {
       $(this).summernote("pasteHTML", "<br><br>");
       e.preventDefault();
    });
});


function post_list(page_num, sr_text){

    let list_form_tag = document.createElement('form');
    list_form_tag.setAttribute('action', $('#list_post_url').val());
    list_form_tag.setAttribute('method', 'post');

    let list_page_tag = document.createElement('input');
    list_page_tag.setAttribute('type', 'hidden');
    list_page_tag.setAttribute('name', 'page_num');
    list_page_tag.setAttribute('value', page_num);

    let search_word = document.createElement('input');
    search_word.setAttribute('type', 'hidden');
    search_word.setAttribute('name', 'search_word');
    search_word.setAttribute('value', sr_text);

    let list_csrf_token = document.createElement('input');
    list_csrf_token.setAttribute('type', 'hidden');
    list_csrf_token.setAttribute('name', 'csrfmiddlewaretoken');
    list_csrf_token.setAttribute('value', $('#csrf_token').val());

    list_form_tag.appendChild(list_page_tag);
    list_form_tag.appendChild(list_csrf_token);
    document.body.appendChild(list_form_tag);
    list_form_tag.submit();
}


function post_detail_info(post_id_value, view_type){
    let form_tag = document.createElement('form');
    form_tag.setAttribute('action', $('#detail_post_url').val());
    form_tag.setAttribute('method', 'post');

    let post_id = document.createElement('input');
    post_id.setAttribute('type', 'hidden');
    post_id.setAttribute('name', 'post_id');
    post_id.setAttribute('value', post_id_value);

    let csrf_token = document.createElement('input');
    csrf_token.setAttribute('type', 'hidden');
    csrf_token.setAttribute('name', 'csrfmiddlewaretoken');
    csrf_token.setAttribute('value', $('#csrf_token').val());

    let view_type_tag = document.createElement('input');
    view_type_tag.setAttribute('type', 'hidden');
    view_type_tag.setAttribute('name', 'view_type');
    view_type_tag.setAttribute('value', view_type);

    form_tag.appendChild(post_id);
    form_tag.appendChild(csrf_token);
    form_tag.appendChild(view_type_tag);
    document.body.appendChild(form_tag);
    form_tag.submit();
}


function post_update(){
    let update_post_url = $('#update_post_url').val();
    let update_form_info = $('#update_post_form')[0];
    let update_form_data = new FormData(update_form_info);

    let input_tags = update_form_info.getElementsByTagName('input');
    for(let i=0; i<input_tags.length; i++){
        let tag_name = input_tags[i].name;
        let tag_value = input_tags[i].value;
        if((tag_name === 'post_title' && tag_value === '') || (tag_name === 'post_cont' && tag_value === '')){
            return alert("정보 미입력 됨");
        }
    }

    $.ajax({
        type        : 'POST',
        url         : update_post_url,
        data        : update_form_data,
        contentType : false,
        processData : false,
        success     : function (data) {
            if(data.result === 'SUCCESS'){
                alert("수정 완료");
                post_detail_info(data.post_id, 'detail');
            }else{
                alert("수정 실패");
            }
        },
        error       : function (error) {
            console.log("error", error);
        }
    });
}


function post_delete(){
    if(!confirm('정말 삭제하시겠습니까?')) return;

    let delete_post_url = $('#delete_post_url').val();
    let post_id = $('#post_id').val();
    let list_post_url = $("#list_post_url").val();
    let csrf_token = $("#csrf_token").val();

    let data_info = {
        'post_id' : post_id
    }
    $.ajax({
        type        : 'POST',
        url         : delete_post_url,
        headers     : {
            "X-CSRFToken" : csrf_token
        },
        data        : JSON.stringify(data_info),
        contentType : false,
        processData : false,
        success     : function (data) {
            if(data.result === 'SUCCESS'){
                alert("삭제 완료");
                window.location.href = list_post_url;
            }else{
                alert("삭제 실패");
            }
        },
        error       : function (error) {
            console.log("error", error);
        }
    });
}


function post_create(){
    let create_post_url = $('#create_post_url').val();
    let form_info = $('#create_post_form')[0];
    let form_data = new FormData(form_info);

    let input_tags = form_info.getElementsByTagName('input');
    for(let i=0; i<input_tags.length; i++){
        let tag_name = input_tags[i].name;
        let tag_value = input_tags[i].value;
        if((tag_name === 'post_title' && tag_value === '') || (tag_name === 'post_cont' && tag_value === '')){
            return alert("제목 정보 미입력 됨");
        }
    }

    $.ajax({
        type        : 'POST',
        url         : create_post_url,
        data        : form_data,
        contentType : false,
        processData : false,
        success     : function (data) {
            if(data.result === 'SUCCESS'){
                alert("등록 완료");
                post_detail_info(data.post_id, 'detail');
            }else{
                alert("등록 실패");
            }
        },
        error       : function (error) {
            console.log("error", error);
        }
    });
}


function post_search(){
    let search_word = $('#search_word').val();
    post_list(1, search_word);
}