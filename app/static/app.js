// RWD Design
const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');

menu.addEventListener('click', function() {
    // 使用 AJAX 請求發送菜單狀態
    const xhr = new XMLHttpRequest();
    const menuState = menu.classList.contains('is-active') ? 'active' : 'inactive';
    const menuLinksState = menuLinks.classList.contains('active') ? 'active' : 'inactive';
    const url = '/toggle_menu?menu_state=' + menuState + '&menu_links_state=' + menuLinksState;

    xhr.open('GET', url, true);
    xhr.send();
});

// 獲取連結
const hsinchuLink = document.querySelector('#hsinchu');
const taichungLink = document.querySelector('#taichung');
const tainanLink = document.querySelector('#tainan');

// 定義共用的點擊事件處理函數
function handle_click(event, url) {
    event.preventDefault(); // 阻止超連結的默認行為
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();

    // 接收響應並更新頁面數據
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // 接收頁面數據
            const response = JSON.parse(xhr.responseText);
            // 更新頁面數據
            update_data(response.data);
            // 更新警告圖示
            // update_warning(response.data);
            
        }
    };
}

// 添加點擊事件監聽器
hsinchuLink.addEventListener('click', function(event) {handle_click(event, '/hsinchu');});
taichungLink.addEventListener('click', function(event) {handle_click(event, '/taichung');});
tainanLink.addEventListener('click', function(event) {handle_click(event, '/tainan');});

function update_data(data) {
    // 獲取需要更新的元素
    const electricityValueElement = document.getElementById('electricity_value');
    const electricityMaximumElement = document.getElementById('electricity_maximum');

    const earthquakeTimeElement = document.getElementById('earthquake_time');
    const earthquakeMagnitudeElement = document.getElementById('earthquake_magnitude');

    const reservoirName1Element = document.getElementById('reservoir_name_1');
    const reservoirPercentage1Element = document.getElementById('reservoir_percentage_1');
    const reservoirTime1Element = document.getElementById('reservoir_time_1');

    const reservoirName2Element = document.getElementById('reservoir_name_2');
    const reservoirPercentage2Element = document.getElementById('reservoir_percentage_2');
    const reservoirTime2Element = document.getElementById('reservoir_time_2');

    const reservoirName3Element = document.getElementById('reservoir_name_3');
    const reservoirPercentage3Element = document.getElementById('reservoir_percentage_3');
    const reservoirTime3Element = document.getElementById('reservoir_time_3');

    // 更新元素的內容為最新的數據
    electricityValueElement.textContent = data.electricity_value;
    electricityMaximumElement.textContent = data.electricity_maximum;
    earthquakeTimeElement.textContent = data.earthquake_time;
    earthquakeMagnitudeElement.textContent = data.earthquake_magnitude;
    reservoirName1Element.textContent = data.reservoir_name_1;
    reservoirPercentage1Element.textContent = data.reservoir_percentage_1;
    reservoirTime1Element.textContent = data.reservoir_time_1;
    reservoirName2Element.textContent = data.reservoir_name_2;
    reservoirPercentage2Element.textContent = data.reservoir_percentage_2;
    reservoirTime2Element.textContent = data.reservoir_time_2;
    reservoirName3Element.textContent = data.reservoir_name_3;
    reservoirPercentage3Element.textContent = data.reservoir_percentage_3;
    reservoirTime3Element.textContent = data.reservoir_time_3;
}

// function update_warning(data) {

//     let elec_warning_percentage = (data.electricity_maximum - data.electricity_value) / data.electricity_value;
//     let elec_extra_capcity = data.electricity_maximum - data.electricity_value
//     if (elec_warning_percentage < 0.1 || elec_extra_capcity < 90) {
//         $("warn_electricity").append('<img class="warning" src="static/Ambox_warning_yellow.svg.png" width="70px" style="background-color: transparent; padding-right:10px"></img>');
//     }

//     $("warn_electricity").append('<img class="warning" src="static/Ambox_warning_yellow.svg.png" width="70px" style="background-color: transparent; padding-right:10px"></img>');

//     if (data.earthquake_magnitude >= 3)
//     {
//         $("warn_earthquake").append('<img class="warning" src="static/Ambox_warning_yellow.svg.png" width="70px" style="background-color: transparent; padding-right:10px"></img>');
//     }

// }

$(".navbar__item > .navbar__links").click(function(){
    $(".navbar__item > .navbar__links").removeClass("active");
    $(this).addClass("active");
});