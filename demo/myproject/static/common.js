$(document).ready(function () {
    $('#inputBox2').click(function () {
        var keyword =  $("#inputText").val()
        var postdata = {
            'keyword':keyword
        }
        console.log(JSON.stringify(postdata))
      // var textDsata = "국민의 권리와 의무  모든 국민은 인간으로서의 존엄과 가치"
        $.ajax({
            type: 'POST',
            url: '/text',
            data: JSON.stringify(postdata),
            dataType : 'JSON',
            contentType: "application/json",
            success: function (data) {
                alert(data) //연결을 확인한다
                //console.log( data)
            },
            error: function(){
                alert('ajax 통신 실패')
            }
        })

    });
})