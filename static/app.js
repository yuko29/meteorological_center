// RWD Design
const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');

menu.addEventListener('click', function() {
  menu.classList.toggle('is-active');
  menuLinks.classList.toggle('active');
});


menu.addEventListener('click', function() {
    // 使用AJAX請求發送菜單狀態
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
            update_data(response.data)
        }
    };
}

// 添加點擊事件監聽器
hsinchuLink.addEventListener('click', function(event) {handle_click(event, '/hsinchu');});
taichungLink.addEventListener('click', function(event) {handle_click(event, '/taichung');});
tainanLink.addEventListener('click', function(event) {handle_click(event, '/tainan');});

function update_data(data) {
    // 獲取需要更新的元素
    const electricityValueElement = document.getElementById('Electricity_value');
    const electricityMaximumElement = document.getElementById('Electricity_maximum');
    const earthquakeTimeElement = document.getElementById('Earthquake_time');
    const earthquakeMagnitudeElement = document.getElementById('Earthquake_magnitude');
    const reservoirName1Element = document.getElementById('Reservoir_name_1');
    const reservoirPercentage1Element = document.getElementById('Reservoir_percentage_1');
    const reservoirName2Element = document.getElementById('Reservoir_name_2');
    const reservoirPercentage2Element = document.getElementById('Reservoir_percentage_2');
    const reservoirName3Element = document.getElementById('Reservoir_name_3');
    const reservoirPercentage3Element = document.getElementById('Reservoir_percentage_3');

    // 更新元素的內容為最新的數據
    electricityValueElement.textContent = data.Electricity_value;
    electricityMaximumElement.textContent = data.Electricity_maximum;
    earthquakeTimeElement.textContent = data.Earthquake_time;
    earthquakeMagnitudeElement.textContent = data.Earthquake_magnitude;
    reservoirName1Element.textContent = data.Reservoir_name_1;
    reservoirPercentage1Element.textContent = data.Reservoir_percentage_1;
    reservoirName2Element.textContent = data.Reservoir_name_2;
    reservoirPercentage2Element.textContent = data.Reservoir_percentage_2;
    reservoirName3Element.textContent = data.Reservoir_name_3;
    reservoirPercentage3Element.textContent = data.Reservoir_percentage_3;
}
