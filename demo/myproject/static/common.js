$(document).ready(function () {
   for(let i =0; i< 50; i++){
        $('#tb').append('<tr><td class="nth_number"></td><td class="data"></td></tr>');
   }
    for(let i =0; i < $('.nth_number').length; i++){
        $('.nth_number')[i].innerText = i + "위"
    }
    
    $('#inputBox2').click(function () {
        var keyword =  $("#inputText").val()
        var postdata = {
            'keyword':keyword
        }
        let asdf  = []
        
        // 유효성 검사 
        if($("#inputText").val() == ""){
            alert("키워드를 입력해주세요")
            $("#inputText").focus()
        }else{
            $.ajax({
                type: 'POST',
                url: '/text',
                data: JSON.stringify(postdata),
                dataType : 'JSON',
                contentType: "application/json",
                success : function(data) {
                    // 입력한 키워드의 빈도수 순위별 데이터 나타내기
                    for(let i = 0; i <data.length; i++){
                        let a= data[i].join(' / ')
                        $('.data')[i].innerText = a
                        asdf.push(a)
                    }
                    console.log(asdf)
                    localStorage.setItem("key", asdf);
                    setInterval(function(){
                        $("#go").css("background-color", "#00ef01")
                        if ($("#go").val() == "보기") {
                            $("#go").val(" ")
                        } else {
                            $("#go").val("보기")
                        }   
                    }, 500) 
                },
                error:function(error){
                    alert("찾을 수 없는 키워드 입니다. 다시 입력해주세요."); 
                    $("#inputText").val(" ")
                    $("#inputText").focus()// 실패 시 처리
                }
                   
            })
            
            // 클릭시 페이지 리로드함
            $('#go').on({'click': function(){
                console.log("click함")
                window.location.reload()
                }
            });
        }
    });
  
    // 전 데이터 새로고침 후에도 유지하기 ( 데이터 테이블  & 이미지 )
    let output = localStorage.getItem("key");		
    let s = output.split(",")
    for(let i = 0; i <s.length; i++){
        $('.data')[i].innerText = s[i]
    }
    $("#wordcloud_img").attr("src", "../static/images/wordcloud_img.png");    
    $("#wordcloud_img").width('100%');
})
