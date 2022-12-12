const popupReg = document.querySelector('.popup-reg');
const headerRegBtn = document.querySelector('.header__register-button');
const popupRegContainer = document.querySelector('.popup-reg__container');

headerRegBtn.addEventListener('click', () => {
  popupReg.classList.add('popup_active');
  console.log('1');
});

popupReg.addEventListener("click", function (e) {
  const target = e.target;
  const its_menu = target == popupRegContainer || popupRegContainer.contains(target);
  const menu_is_active = popupReg.classList.contains("popup_active");

  if (!its_menu && menu_is_active) {
      popupReg.classList.remove('popup_active');
      console.log('2');
  }
});



const popupLoginToggleBtn = document.querySelector('.popup-reg__login');
const popupLogin = document.querySelector('.popup-log');
const popupLogContainer = document.querySelector('.popup-log__container');

popupLoginToggleBtn.addEventListener('click', (evt) => {
  evt.preventDefault();
  popupReg.classList.remove('popup_active');
  popupLogin.classList.add('popup_active');
})

const popupRegToggleBtn = document.querySelector('.popup-log__register');

popupRegToggleBtn.addEventListener('click', (evt) => {
  evt.preventDefault();
  popupLogin.classList.remove('popup_active');
  popupReg.classList.add('popup_active');
});

popupLogin.addEventListener("click", function (e) {
  const target = e.target;
  const its_menu = target == popupLogContainer || popupLogContainer.contains(target);
  const menu_is_active = popupLogin.classList.contains("popup_active");

  if (!its_menu && menu_is_active) {
      popupLogin.classList.remove('popup_active');
      console.log('2');
  }
});

const popupCloseBtn = document.querySelector('.popup__close');
const popupCloseBtn2 = document.querySelector('.popup__close2');
popupCloseBtn.addEventListener('click', () => {
  popupReg.classList.remove('popup_active');
});
popupCloseBtn2.addEventListener('click', () => {
  popupLogin.classList.remove('popup_active');
});

const allSportsBtn = document.querySelector('.translations__sport-chose-btn_type_all');
const footbalSportBtn = document.querySelector('.translations__sport-chose-btn_type_football');
const hockeySportBtn = document.querySelector('.translations__sport-chose-btn_type_hockey');
allSportsBtn.addEventListener('click', () => {
  allSportsBtn.classList.add('translations__sport-choose_active');
  footbalSportBtn.classList.remove('translations__sport-choose_active');
  hockeySportBtn.classList.remove('translations__sport-choose_active');
});
footbalSportBtn.addEventListener('click', () => {
  footbalSportBtn.classList.add('translations__sport-choose_active');
  allSportsBtn.classList.remove('translations__sport-choose_active');
  hockeySportBtn.classList.remove('translations__sport-choose_active');
});
hockeySportBtn.addEventListener('click', () => {
  hockeySportBtn.classList.add('translations__sport-choose_active');
  footbalSportBtn.classList.remove('translations__sport-choose_active');
  allSportsBtn.classList.remove('translations__sport-choose_active');
});

const todayChooseBtn = document.querySelector('.translations__date-choose-btn_type_today');
const yesterdayChooseBtn = document.querySelector('.translations__date-choose-btn_type_yesterday');
const tomorrowChooseBtn = document.querySelector('.translations__date-choose-btn_type_tomorrow');
todayChooseBtn.addEventListener('click', () => {
  todayChooseBtn.classList.add('translations__date-choose_active');
  yesterdayChooseBtn.classList.remove('translations__date-choose_active');
  tomorrowChooseBtn.classList.remove('translations__date-choose_active');
});
yesterdayChooseBtn.addEventListener('click', () => {
  yesterdayChooseBtn.classList.add('translations__date-choose_active');
  todayChooseBtn.classList.remove('translations__date-choose_active');
  tomorrowChooseBtn.classList.remove('translations__date-choose_active');
});
tomorrowChooseBtn.addEventListener('click', () => {
  tomorrowChooseBtn.classList.add('translations__date-choose_active');
  yesterdayChooseBtn.classList.remove('translations__date-choose_active');
  todayChooseBtn.classList.remove('translations__date-choose_active');
});

const newsSportAll = document.querySelector('.news__sport-chose-btn_type_all');
const newsSportFootbal = document.querySelector('.news__sport-chose-btn_type_footbal');
const newsSportHockey = document.querySelector('.news__sport-chose-btn_type_hockey');
newsSportAll.addEventListener('click', () => {
  newsSportAll.classList.add('translations__sport-choose_active');
  newsSportFootbal.classList.remove('translations__sport-choose_active');
  newsSportHockey.classList.remove('translations__sport-choose_active');
});
newsSportFootbal.addEventListener('click', () => {
  newsSportFootbal.classList.add('translations__sport-choose_active');
  newsSportAll.classList.remove('translations__sport-choose_active');
  newsSportHockey.classList.remove('translations__sport-choose_active');
});
newsSportHockey.addEventListener('click', () => {
  newsSportHockey.classList.add('translations__sport-choose_active');
  newsSportFootbal.classList.remove('translations__sport-choose_active');
  newsSportAll.classList.remove('translations__sport-choose_active');
});


const searchingForm = document.querySelector('.searching-form');
const poiskInput = document.querySelector('.poisk__input');
searchingForm.addEventListener('submit', (evt) => {
  evt.preventDefault();
  window.open('./search.html');
  poiskInput.value = searchingForm.value;
});

