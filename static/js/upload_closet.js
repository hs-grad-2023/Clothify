// ===== file reader =====
function readURL(input) {
    if (input.files && input.files[0]) {

        var reader = new FileReader();

        reader.onload = function (e) {
            $('.image-upload-wrap').hide();

            $('.file-upload-image').attr('src', e.target.result);
            $('.file-upload-content').show();

            $('.image-title').html(input.files[0].name);
        };

        reader.readAsDataURL(input.files[0]);

    } else {
        removeUpload();
    }
}

function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});

function addImage() {
    document.querySelector('.file-upload-input').click();
}

// ===== form 유효성 테스트 =====

// const submitform = document.querySelector("#clothes_info"); // form을 sumitform 변수에 저장
 
// submitform.addEventListener("submit",validationData) 
// // form이 submit되면 submitPhoto함수를 실행하겠다고 선언
 
// function validationData(event){
//     alert("모야ㅐ");
//     event.preventDefault(); //여기서 자동 submit을 막아줍니다.
//     const clothes_info = {
//     season : submitform.querySelector('#season'),
//     type1 : submitform.querySelector('#type1'),
//     type2 : submitform.querySelector('#type2'),
//     tag : submitform.querySelector('#tags'),
//     name : submitform.querySelector('#name'),
//     imgfile : submitform.querySelector('#imgfile'),
//     details : submitform.querySelector('#details'),
//     };

//     if(clothes_info[0].value == "" ){ // input form이 비어있으면
//         alert("분류1을 선택하지 않았습니다."); //이 부분에 알림창 띄우는 코드를 작성해 줄 예정입니다
//     }else if(clothes_info[1].value == "" ){ // input form이 비어있으면
//         alert("분류2을 선택하지 않았습니다."); //이 부분에 알림창 띄우는 코드를 작성해 줄 예정입니다
//     }else if(imgInput.value != ""){ // 사진이 있으면?
//         submitform.submit(); //정상적으로 submit으로 넘어가겠습니다!
//     }

// }

// ===== button function =====

$(document).ready(function() {
    $('.btn-submit').click(function() {
      $('.btnText').html('Done');
      $('.btn-submit').addClass('btn-active');
    });
  });


// ===== tag =====

function addtag(){ //유효성 검사 + 엔터 누르면 tag label에 추가시키는 코드
    var value = $('#tag').val();
    var valuelist = $('#tags').val();
    var reg = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi;
    var tagvalue = value.replace(reg, "");

    if (value=''|| value==null || value ==false){
        alert("추가할 tag를 입력해주세요.");
    }else{
        if (valuelist==''){
            $('#tags').val('#' + tagvalue);
        }
        else{
            $('#tags').val(valuelist+', #'+tagvalue);
        }
    }

    $('#tag').val('');
}


// ===== type2 option =====
function itemChange(){

    var top = ["=== 분류2 ===","니트/스웨터","셔츠/블라우스","후드 티셔츠", "피케/카라 티셔츠","맨투맨/스웨트셔츠", "반소매 티셔츠","긴소매 티셔츠","민소매 티셔츠","기타 상의"];
    var pants = ["=== 분류2 ===","데님 팬츠","숏 팬츠","코튼 팬츠", "레깅스","슈트 팬츠/슬랙스","점프 슈트/오버올","트레이닝/조거 팬츠","기타 바지"];
    var skirt = ["=== 분류2 ===","미니 스커트", "미디 스커트","롱 스커트"];
    var dress = ["=== 분류2 ===","미니 원피스", "미디 원피스","맥시 원피스"];
    var outer = ["=== 분류2 ===","후드 집업","환절기 코트", "블루종/MA-1","겨울 코트", "레더/라이더스 재킷","무스탕/퍼","롱패딩/롱헤비 아우터","슈트/블레이저 재킷","숏패딩/숏헤비 아우터","카디건","아노락 재킷","패딩 베스트","플리스/뽀글이","트레이닝 재킷","기타 아우터"];
    var bag = ["=== 분류2 ===","백팩","메신저/크로스 백","파우치 백","숄더백","에코백","토트백","클로치 백","웨이스트백/힙색"];
    var accessary = ["=== 분류2 ===","모자","레그웨어","머플러","장갑","시계","팔찌","귀걸이","반지","발찌","목걸이","헤어 액세서리"];
    var shoes = ["=== 분류2 ===","구두","샌들","로퍼","힐/펌프스","플랫 슈즈","부츠","캔버스/단화","스포츠 스니커즈"];

    var selectItem = $("#type1").val();
    alert(selectItem);
    var changeItem;
      
    if(selectItem == "top"){
      changeItem = top;
    }
    else if(selectItem == "pants"){
      changeItem = pants;
    }
    else if(selectItem == "skirt"){
      changeItem =  skirt;
    }
    else if(selectItem == "dress"){
        changeItem = dress;
    }
    else if(selectItem == "outer"){
        changeItem = outer;
    }
    else if(selectItem == "bag"){
        changeItem = bag;
    }
    else if(selectItem == "accessary"){
        changeItem = accessary;
    }
    else if(selectItem == "shoes"){
        changeItem = shoes;
    }
     
    $('#type2').empty();
     
    for(var count = 0; count < changeItem.length; count++){                
                    var option = $("<option>"+changeItem[count]+"</option>");
                    $('#type2').append(option);
                }
     
    }
    