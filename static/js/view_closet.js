typeCategory = {
        '상의':  ["니트/스웨터","셔츠/블라우스","후드 티셔츠", "피케/카라 티셔츠","맨투맨/스웨트셔츠", "반소매 티셔츠","긴소매 티셔츠","민소매 티셔츠","기타 상의"],
        '하의': ["데님 팬츠","숏 팬츠","코튼 팬츠", "레깅스","슈트 팬츠/슬랙스","점프 슈트/오버올","트레이닝/조거 팬츠","기타 바지"],
        '치마': ["미니 스커트", "미디 스커트","롱 스커트"],
        '원피스': ["미니 원피스", "미디 원피스","맥시 원피스"],
        '아우터': ["후드 집업","환절기 코트", "블루종/MA-1","겨울 코트", "레더/라이더스 재킷","무스탕/퍼","롱패딩/롱헤비 아우터","슈트/블레이저 재킷","숏패딩/숏헤비 아우터","카디건","아노락 재킷","패딩 베스트","플리스/뽀글이","트레이닝 재킷","기타 아우터"],
        '가방': ["백팩","메신저/크로스 백","파우치 백","숄더백","에코백","토트백","클로치 백","웨이스트백/힙색"],
        '악세서리': ["모자","레그웨어","머플러","장갑","시계","팔찌","귀걸이","반지","발찌","목걸이","헤어 액세서리"],
        '신발': ["구두","샌들","로퍼","힐/펌프스","플랫 슈즈","부츠","캔버스/단화","스포츠 스니커즈"],
}


var selectedType1 = []; //type2 필터
var selectedFilter = []; //최종 필터


//동적으로 type2 삽입하기
function addType2(type1_val, optLen) {
    // select 엘리먼트 가져오기
    var type2_element = document.getElementById("type2");

    //선택리스트 만들기
    if (!(type1_val in selectedType1)) { //type1이 선택되지 않았으면
        selectedType1.push(type1_val);
    } else { }//type1이 이미 선택됐으면

    // 새로운 option 엘리먼트 생성하기
    if (selectedType1.length <= 2) {
        for (let i = 0; i < optLen; i++) { //type2의 개수(삽입할 옵션개수)만큼 반복
            //$('.type2_box').multiSelect('addOption',(typeCategory[type1_val][i]));
            //한번 추가했다가 지우면 다시 추가가 안됨.. 

            let newOption = document.createElement("option");
            newOption.text = typeCategory[type1_val][i];

            // option 엘리먼트를 select 엘리먼트에 추가하기
            type2_element.add(newOption);
        }
    }
}

//기존 type2 삭제하기
function delType2(type1_val, optLen) {
    if (selectedType1.length >= 2) {
        var oldElement = selectedType1.shift();

        const citySelect = document.getElementById("type2");
        console.log('citySelect.options: ', citySelect.options.length)
        for (let i = 0; i < optLen; i++) {
            citySelect.remove(citySelect.options[citySelect.options.length - 1]);
        }
    }
}

// selected 추가하는 함수
function addSelected() {
    const type2_element = document.getElementById("type2"); //선택한 옵션값
    const type2_val = type2_element.value; //선택한 옵션값
    const selected_element = document.getElementById("selected"); //추가할 요소

    // 선택 리스트 만들기
    selectedFilter.push(type2_val);

    // 선택된 리스트는 숨기기
    const selectedOption = type2_element.selectedIndex;
    type2_element.options[selectedOption].hidden = true;

    // 새로운 option 엘리먼트 생성하기
    let newOption = document.createElement("option");
    newOption.text = type2_val;
    // option 엘리먼트를 select 엘리먼트에 추가하기
    selected_element.add(newOption);


}

// selected 삭제하는 함수
function delSelected() {
    const type1_val = document.getElementById("type1").value;
    const optLen = typeCategory[type1_val].length; //getType에서 type1값을 가져옴
    const type2_element = document.getElementById("type2"); //선택한 옵션값
    const type2_val = type2_element.value;
    const selected_element = document.getElementById("selected"); //다시 취소할 옵션 요소
    const selected_val = selected_element.value; //취소할 옵션값

    //selectedFilter에서 옵션을 삭제
    for (let i = 0; i < selectedFilter.length; i++) {
        if (selectedFilter[i] == selected_val) {
            selectedFilter.splice(i, 1);
            break;
        }
    }

    //type2에 옵션 되돌리기
    for (let i = 0; i < optLen; i++) { //type2의 개수(삽입할 옵션개수)만큼 반복
        if (typeCategory[type1_val][i] == type2_val) {
            type2_element.options[i].hidden = false;
            break;
        }
    }
    const selectedOption = selected_element.selectedIndex;
    selected_element.remove(selected_element.options[selectedOption]);


}

//type1으로 type2 추가
document.getElementById("type1").addEventListener("click", function () {
    var type1_val = document.getElementById("type1").value;
    var optLen = typeCategory[type1_val].length; //getType에서 type1값을 가져옴

    addType2(type1_val, optLen);
    delType2(type1_val, optLen);
})

//type2로 selected 추가
document.getElementById("type2").addEventListener("click", function () {

    addSelected();
})

//selected 제거
document.getElementById("selected").addEventListener("click", function () {

    delSelected();
})

