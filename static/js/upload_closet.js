window.onload=function(){

    // ===== file reader =====

    var formInfo = document.getElementsByName("FormInfo").item; // form을 sumitform 변수에 저장

    console.log(formInfo);

    // ===== form 유효성 테스트 =====
    var validationData_value = false;
    var submitform = document.getElementById("clothesInfo"); // form을 sumitform 변수에 저장
    
    submitform.addEventListener("submit",validationData) 
    // form이 submit되면 submitPhoto함수를 실행하겠다고 선언

    function Request(valuename)
    {
        var rtnval;
        var nowAddress = unescape(location.href);
        var parameters = new Array();
        parameters = (nowAddress.slice(nowAddress.indexOf("?")+1,nowAddress.length)).split("&");
        for(var i = 0 ; i < parameters.length ; i++){
            if(parameters[i].split("=")[0] == valuename){
                rtnval = parameters[i].split("=")[1];
                if(rtnval == undefined || rtnval == null){
                    rtnval = "";
                }
                return rtnval;
            }
        }
    }

    function validationData(event){
        event.preventDefault(); //여기서 자동 submit을 막아줍니다.
        console.log(Request("imgfile"));
        if($('#type1').val() == "" || $('#type1').val() == "none" || $('#type1').val() == null){ // input form이 비어있으면
            alert("분류1을 선택하지 않았습니다."); 
            validationData_value= false;
        }else if($('#type2').val() == "" || $('#type2').val() == "none" || $('#type2').val() == null){ // input form이 비어있으면
            alert("분류2을 선택하지 않았습니다."); 
            validationData_value= false;
        }else if($('#clothesName').val() == "" || $('#clothesName').val() == "none" || $('#clothesName').val() == null){ // input form이 비어있으면
            alert("이름을 입력하지 않았습니다."); 
            validationData_value= false;
            /*
        }else if(Request.POST("imgfile") == "" || Request.POST("imgfile") == null){ // input form이 비어있으면
            
            alert("이미지가 없습니다."); 
            validationData_value= false;
            var name = Request.POST("imgfile");
        }else if($('#imgfile').val() != ""){ // 사진이 있으면?
            */
        }else{ // 사진이 있으면?
            submitform.submit(); //정상적으로 submit으로 넘어가겠습니다!
            validationData_value= true;
        }   
    }

    // ===== button function =====



    document.getElementById("btn-submit").addEventListener("click", function(){
        if(validationData_value){
            document.getElementById("btnText").innerHTML = "Done";
            document.getElementById("btn-submit").addClass('btn-active');
        }
    });
    document.getElementById("btn-submit").addEventListener("keyup", addtag);
    document.addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            addtag();
        }
      });


    const btn_addtag = document.getElementsByClassName("btn_addtag")
    if (btn_addtag){
        for (let i = 0; i < btn_addtag.length; i++) {
            btn_addtag[i].addEventListener("click", addtag);
        }
    }
    const btn_deltag = document.getElementsByClassName("tag_delete")
    if (btn_deltag){
        for (let i = 0; i < btn_deltag.length; i++) {
            btn_deltag[i].addEventListener("click", deletetag);
        }
    }


    
    // ===== tag =====
    function addtag(){ //유효성 검사 + 엔터 누르면 tag label에 추가시키는 코드
        var value = $('#tag').val();
        var valuelist = $('#tags').val();
        var tagarea = document.getElementsByClassName("tag_area")[0];
        var reg = /[\s\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi;
        var tagvalue = value.replace(reg, "");

        if (value===''|| value==null || value ==false){
            alert("추가할 tag를 입력해주세요.");
        }else{
            if (valuelist==''){
                $('#tags').val('#' + tagvalue);
            }
            else{
                $('#tags').val(valuelist+', #'+tagvalue);
            }
            const btnElement = document.createElement('button');
            btnElement.type = "button";
            btnElement.classList.add("tag_btn");
            btnElement.innerHTML = '<span class="tag_text">#' + tagvalue + '</span><i class="fa-sharp fa-solid fa-xmark tag_delete"></i>';
            tagarea.appendChild(btnElement);

            const cnt_tag = document.getElementsByClassName("tag_delete").length -1
            document.getElementsByClassName("tag_delete")[cnt_tag].addEventListener("click", deletetag);
            
            document.getElementsByClassName('tag_btn')[cnt_tag].style.borderRadius = '30px';
            document.getElementsByClassName('tag_btn')[cnt_tag].style.border = '1px solid gray';
            document.getElementsByClassName('tag_btn')[cnt_tag].style.marginRight = '15px';
            document.getElementsByClassName('tag_btn')[cnt_tag].style.marginTop = '10px';
            document.getElementsByClassName('tag_btn')[cnt_tag].style.padding = '10px';
            document.getElementsByClassName('tag_delete')[cnt_tag].style.marginLeft = '10px';
            
        $('#tag').val('');
        }
    }

    function deletetag(){
        //var tag = document.getElementsByClassName('tag_delete');
        var tags_list = document.getElementById('tags').value;
        var delete_tag = this.previousSibling.textContent;
        
        if(tags_list.indexOf(',')!=-1){
            tags_list = tags_list.replace(', '+delete_tag,'');
        }else{
            tags_list = '';
        }
        document.getElementById('tags').value = tags_list;
        // console.log(tags_list);
        this.parentNode.remove();
    }

    document.getElementById("type1").addEventListener("change", itemChange);
    // ===== type2 option =====
    function itemChange(){

        var top = ["=== 분류 2 ===","니트/스웨터","셔츠/블라우스","후드 티셔츠", "피케/카라 티셔츠","맨투맨/스웨트셔츠", "반소매 티셔츠","긴소매 티셔츠","민소매 티셔츠","기타 상의"];
        var pants = ["=== 분류 2 ===","데님 팬츠","숏 팬츠","코튼 팬츠", "레깅스","슈트 팬츠/슬랙스","점프 슈트/오버올","트레이닝/조거 팬츠","기타 바지"];
        var skirt = ["=== 분류 2 ===","미니 스커트", "미디 스커트","롱 스커트"];
        var dress = ["=== 분류 2 ===","미니 원피스", "미디 원피스","맥시 원피스"];
        var outer = ["=== 분류 2 ===","후드 집업","환절기 코트", "블루종/MA-1","겨울 코트", "레더/라이더스 재킷","무스탕/퍼","롱패딩/롱헤비 아우터","슈트/블레이저 재킷","숏패딩/숏헤비 아우터","카디건","아노락 재킷","패딩 베스트","플리스/뽀글이","트레이닝 재킷","기타 아우터"];
        var bag = ["=== 분류 2 ===","백팩","메신저/크로스 백","파우치 백","숄더백","에코백","토트백","클로치 백","웨이스트백/힙색"];
        var accessary = ["=== 분류 2 ===","모자","레그웨어","머플러","장갑","시계","팔찌","귀걸이","반지","발찌","목걸이","헤어 액세서리"];
        var shoes = ["=== 분류 2 ===","구두","샌들","로퍼","힐/펌프스","플랫 슈즈","부츠","캔버스/단화","스포츠 스니커즈"];

        var selectItem = $("#type1").val();
        var changeItem;
        
        if(selectItem == "상의"){
        changeItem = top;
        }
        else if(selectItem == "바지"){
        changeItem = pants;
        }
        else if(selectItem == "치마"){
        changeItem =  skirt;
        }
        else if(selectItem == "원피스"){
            changeItem = dress;
        }
        else if(selectItem == "아우터"){
            changeItem = outer;
        }
        else if(selectItem == "가방"){
            changeItem = bag;
        }
        else if(selectItem == "악세서리"){
            changeItem = accessary;
        }
        else if(selectItem == "신발"){
            changeItem = shoes;
        }
        
        $('#type2').empty();
        
        for(var count = 0; count < changeItem.length; count++){                
                        var option = $("<option>"+changeItem[count]+"</option>");
                        $('#type2').append(option);
                    }
        
    }
}