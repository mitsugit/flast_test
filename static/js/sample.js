$(function(){
 
    /* ここにjQueryのコードを書く */

    $('#jqtest').click(function() {
        let test2 = $('#jq2').val();
        console.log(test2);
        $('#jq1').val(test2);
    })



$('.checkbox').change(function() {
    
    $('.checkbox').each(function() {
        // ページ内のすべてのcheckboxのvalue
        var v = $(this).val();
        //checkされているかどうか
        var isCheck = $(this).prop('checked');
        const stname = "checkbox" + v
        sessionStorage.setItem(stname,isCheck)

    })
    
})

// display form
jQuery(document).ready(function() {
    console.log('test');
    $('.checkbox').each(function(){
        var v = $(this).val();
        const stname = "checkbox" + v;
        console.log(stname);
        let bool = sessionStorage.getItem(stname);
        if(bool == "false") bool = false // 文字列の"false"をfalseに直す
        $(this).prop('checked', bool);  // checkedに文字列が渡されるとチェックマークが付く
    })
    });
    
// 2. チェックの付いたidのoutputフィールドにリストを表示する。

$("#set").click(function() {
    local_checked_list = [];
    for( var key in sessionStorage ){
        target_var = sessionStorage.getItem(key)
   
        if (target_var == "true"){
           let target_key = key.replace("checkbox", "");
           local_checked_list.push(target_key)
        }
   
       }
    
    
    $('#output').val(local_checked_list);

});



// 別イベントからsetを発火
$('#trigger_set').click(function(){
    $('#set').trigger('click');
})



})