const mailCommonModule = (() => {
    // let counter = 0;
    return {
        saveSession: () => {
            // カプセル化することで該当のdomがなくてもjs読込時にエラーにならないメリット。
            // jqueryも使える。
            $('.checkbox').each(function() {
                // ページ内のすべてのcheckboxのvalue
                var v = $(this).val();
                //checkされているかどうか
                var isCheck = $(this).prop('checked');
                const stname = "checkbox" + v
                sessionStorage.setItem(stname,isCheck)
        
            })
        },
        selectMenu: () => {
            $('#jq1').val("test");
            console.log("ヘッダーのメニューが選択されました！")
        },

        displayForm: () => {
            
            $('.checkbox').each(function(){
                var v = $(this).val();
                const stname = "checkbox" + v;
                console.log(stname);
                let bool = sessionStorage.getItem(stname);
                if(bool == "false") bool = false // 文字列の"false"をfalseに直す
                $(this).prop('checked', bool);  // checkedに文字列が渡されるとチェックマークが付く
            })
        },
        // 2. チェックの付いたidのoutputフィールドにリストを表示する。
        set_to_form: () => {
            local_checked_list = [];
            for( var key in sessionStorage ){
                target_var = sessionStorage.getItem(key)
                if (target_var == "true"){
                let target_key = key.replace("checkbox", "");
                local_checked_list.push(target_key)
                }
            }
            $('#output').val(local_checked_list);
        },
        // 3.session false
        delete_storage: () => {
            for( var key in sessionStorage ){
                console.log(key)
                sessionStorage.setItem(key,false)
                }
            
            $('.checkbox').each(function(){
                $(this).prop('checked', false);
            })

            $("#output").value = "";
            // チェックボックスに反映
        }
    }
})();


// イベント定義はここに
$('.checkbox').change(function() {
    mailCommonModule.saveSession();
});
$("#set").click(function() {
    mailCommonModule.set_to_form();
});
$('#deletebtn').click(function(){
    mailCommonModule.delete_storage();
    mailCommonModule.displayForm();
});