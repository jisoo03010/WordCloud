$(document).ready(function () {
    for (let i = 0; i < 50; i++) {
        $('#tb').append('<tr><td class="nth_number"></td><td class="data"></td></tr>');
    }
    for (let i = 0; i < $('.nth_number').length; i++) {
        $('.nth_number')[i].innerText = i + "위"
    }

    $('#inputText').on("keydown", function (key) {
        if (key.keyCode == 13) {
            var keyword = $("#inputText").val()

            var postdata = {
                'keyword': keyword
            }
            let asdf = []

            // 유효성 검사 
            if ($("#inputText").val() == "") {
                alert("키워드를 입력해주세요")
                $("#inputText").focus()
            } else {
                $.ajax({
                    type: 'POST',
                    url: '/text',
                    data: JSON.stringify(postdata),
                    dataType: 'JSON',
                    contentType: "application/json",
                    success: function (data) {
                        jsonData = JSON.parse(data)
                        for (var i=0; i<jsonData.length; i++) {
                            var keykeyw = jsonData[i]['keyword']
                            var value = jsonData[i]['count']
                            putdata = keykeyw + " / " + value
                            
                            $('.data')[i].innerText = putdata
                            asdf.push(putdata)
                        }
                        localStorage.setItem("key", asdf);
                        
                        if (key.keyCode == 13) {
                            console.log("click함")
                            window.location.reload()
                        }
                    },
                    error: function (error) {
                        alert("찾을 수 없는 키워드 입니다. 다시 입력해주세요.");
                        $("#inputText").val(" ")
                        $("#inputText").focus() // 실패 시 처리
                    }
                })

                        
                
            }
        }

        

    });
    // 전 데이터 새로고침 후에도 유지하기 ( 데이터 테이블  & 이미지 )



    let output = localStorage.getItem("key");
    let s = output.split(",")
    for (let i = 0; i < s.length; i++) {
        $('.data')[i].innerText = s[i]
    }
    $("#wordcloud_img").attr("src", "../static/images/wordcloud_img.png");
    $("#wordcloud_img").width('100%');


})

$(document).ready(function () { // 최초 진입 시 로딩바 div를 hide시킨다.
        $('#loading_bar_box').hide();
    })
    .ajaxStart(function () { // ajax 통신 시작 callback (로딩바 show)
        console.log('start');
        $('#loading_bar_box').show();
    })
    .ajaxStop(function () { // ajax 통신 완료 callback (로딩바 hide)
        console.log('end');
        $('#loading_bar_box').hide();
    })
