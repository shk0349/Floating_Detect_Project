// 팀 프로젝트 - 부유물 전용 Javascript
  // 오늘 날짜 표시
  function getTodayKor() {
    let cd = new Date();
    let yr = cd.getFullYear();
    let mh = cd.getMonth() + 1;
    let dt = cd.getDate();
    let today = yr + "년 " + mh + "월 " + dt + "일";

    return today;    
  }

  // 표시 내용 전환

  // 관리자 페이지 이동
  function changeTable(toChange) {
    let showTable = null; // 정보 보이기
    let hideTable = null; // 정보 숨기기

    // 전체 정보 보기
    if(toChange == 'all') {
      hideTable = document.getElementById("todayDetected")
      showTable = document.getElementById("totalDetected")

   // 오늘 정보 보기
    } else {
      hideTable = document.getElementById("totalDetected")
      showTable = document.getElementById("todayDetected")
    }

    hideTable.classList.add("toHide")
    showTable.classList.remove("toHide")
  }